from typing import Any, Dict, List
from collections import defaultdict
from app.services.frappe_client import FrappeClient


# Normalized domain mapping according to Frappe v2.0.0 specification
DOMAIN_MAPPING = {
    "health": "health",
    "health_daily_record": "health",
    "health daily record": "health",
    "activity": "activity",
    "health_activity": "activity",
    "health activity": "activity",
    "financial": "financial",
    "financial_transaction": "financial",
    "financial transaction": "financial",
    "financial_snapshot": "financial_snapshot",
    "financial snapshot": "financial_snapshot",
    "social": "social",
    "social_activity": "social",
    "social activity": "social",
    "wellbeing": "wellbeing",
    "subjective_wellbeing_checkin": "wellbeing",
    "subjective wellbeing checkin": "wellbeing",
}


def build_store_ai_payload(records: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Groups extracted records by canonical domain key according to Frappe v2.0.0 store_ai_record format:
    {
      "health": {...},
      "financial": [{...}, {...}],
      "social": {...},
      "wellbeing": {...},
      "activity": {...}
    }
    """
    domain_groups = defaultdict(list)

    for rec in records:
        raw_domain = (rec.get("domain") or rec.get("doctype") or "health").lower().strip()
        canonical_domain = DOMAIN_MAPPING.get(raw_domain, raw_domain)
        record_data = rec.get("record_data", rec)
        domain_groups[canonical_domain].append(record_data)

    payload: Dict[str, Any] = {}
    for domain, items in domain_groups.items():
        # DocTypes that naturally support multiple entries per day (transactions, activities, social)
        if len(items) == 1:
            # If single item, can be sent as object directly, or list if transactions
            if domain in ("financial", "activity"):
                payload[domain] = items
            else:
                payload[domain] = items[0]
        else:
            payload[domain] = items

    return payload


async def dispatch_records_to_frappe(
    records: List[Dict[str, Any]],
    raw_token: str
) -> List[Dict[str, Any]]:
    """
    Dispatches extracted domain records to Frappe v2.0.0 store_ai_record endpoint.
    Returns structured results including created items and recalculated scores.
    """
    if not records:
        return []

    payload = build_store_ai_payload(records)

    try:
        frappe_res = await FrappeClient.store_ai_record(payload=payload, token=raw_token)

        # In Frappe standard envelope, response is inside 'message' or directly returned
        data = frappe_res.get("data") if isinstance(frappe_res, dict) and "data" in frappe_res else frappe_res
        msg = frappe_res.get("message", "Records processed successfully") if isinstance(frappe_res, dict) else "Success"

        return [{
            "type": "store_ai_record",
            "status": "success",
            "message": msg,
            "data": data,
            "recalculated_scores": data.get("recalculated_scores") if isinstance(data, dict) else None,
        }]

    except Exception as exc:
        return [{
            "type": "store_ai_record",
            "status": "error",
            "error_detail": str(exc),
        }]
