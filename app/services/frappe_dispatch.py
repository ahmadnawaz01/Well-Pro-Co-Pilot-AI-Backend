import asyncio
from typing import Any, Dict, List
import httpx
from app.core.config import settings

async def dispatch_records_to_frappe(
    records: List[Dict[str, Any]],
    raw_token: str
) -> List[Dict[str, Any]]:
    """
    Dispatches extracted domain records to the Frappe RPC endpoint.
    - If multiple records exist, sends a single batch payload using `"atomic": True`.
    - If a single record exists, sends the single-extraction payload.
    """
    if not records:
        return []

    frappe_endpoint = f"{settings.FRAPPE_BASE_URL}/api/method/well_pro.well_pro_app.api.store_ai_record"
    headers = {
        "Authorization": raw_token,
        "Content-Type": "application/json",
    }

    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            # Case A: Batch Extraction (Multiple Records)
            if len(records) > 1:
                batch_records = []
                for rec in records:
                    batch_records.append({
                        "domain": rec.get("domain"),
                        "record_data": rec.get("record_data", {})
                    })

                payload = {
                    "atomic": True,
                    "records": batch_records
                }

                response = await client.post(frappe_endpoint, json=payload, headers=headers)
                if response.status_code == 200:
                    res_json = response.json()
                    msg_wrapper = res_json.get("message", {})
                    return [{
                        "type": "batch",
                        "status": "success",
                        "message": msg_wrapper.get("message", "Batch records inserted successfully"),
                        "data": msg_wrapper.get("data")
                    }]
                else:
                    return [{
                        "type": "batch",
                        "status": "error",
                        "status_code": response.status_code,
                        "error_detail": response.text
                    }]

            # Case B: Single Extraction (One Record)
            else:
                single_rec = records[0]
                domain = single_rec.get("domain")
                payload = {
                    "domain": domain,
                    "record_data": single_rec.get("record_data", {})
                }

                response = await client.post(frappe_endpoint, json=payload, headers=headers)
                if response.status_code == 200:
                    res_json = response.json()
                    msg_wrapper = res_json.get("message", {})
                    return [{
                        "domain": domain,
                        "status": "success",
                        "message": msg_wrapper.get("message", "Record inserted successfully"),
                        "data": msg_wrapper.get("data")
                    }]
                else:
                    return [{
                        "domain": domain,
                        "status": "error",
                        "status_code": response.status_code,
                        "error_detail": response.text
                    }]

        except Exception as exc:
            return [{
                "status": "error",
                "error_detail": str(exc)
            }]