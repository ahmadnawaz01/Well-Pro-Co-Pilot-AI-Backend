import json
import httpx
from typing import Optional, Dict, Any, List
from langchain_core.tools import tool
from langchain_core.runnables import RunnableConfig
from app.core.config import settings


def _get_headers(config: RunnableConfig) -> Dict[str, str]:
    """Retrieves caller's Frappe token from LangGraph runtime config context."""
    token = config.get("configurable", {}).get("frappe_token")
    if not token:
        raise ValueError("Authentication token missing from session context.")
    return {
        "Authorization": token,
        "Content-Type": "application/json"
    }


@tool
async def get_user_records_tool(
    doctype: str, 
    from_date: Optional[str] = None, 
    to_date: Optional[str] = None, 
    limit: int = 20, 
    config: RunnableConfig = None
) -> str:
    """
    Fetch user records from Frappe for question-answering or viewing history.
    doctype: Allowed DocTypes: 'Health Daily Record', 'Health Activity', 'Financial Transaction', 
             'Financial Snapshot', 'Social Activity', 'Subjective Wellbeing Checkin'.
    from_date / to_date: Optional YYYY-MM-DD string filters.
    """
    headers = _get_headers(config)
    url = f"{settings.FRAPPE_BASE_URL}/api/method/well_pro.well_pro_app.api.get_user_records"
    params = {"doctype": doctype, "limit": limit}
    if from_date:
        params["from_date"] = from_date
    if to_date:
        params["to_date"] = to_date

    async with httpx.AsyncClient(timeout=10.0) as client:
        res = await client.get(url, headers=headers, params=params)
        if res.status_code == 200:
            data = res.json().get("message", {}).get("data", [])
            return json.dumps(data, indent=2)
        return f"Error fetching records ({res.status_code}): {res.text}"


@tool
async def insert_user_records_tool(
    records: List[Dict[str, Any]], 
    atomic: bool = True, 
    config: RunnableConfig = None
) -> str:
    """
    Insert single or batch records into Frappe using the store_ai_record batch endpoint.
    records: List of dicts, each with keys 'domain' ('health', 'health_activity', 'financial', 'social', 'wellbeing')
             and 'record_data' dict conforming to the schema.
    Example:
    records = [
      {"domain": "financial", "record_data": {"transaction_type": "Expense", "amount": 12.0, ...}},
      {"domain": "health_activity", "record_data": {"activity_type": "Running", "duration_minutes": 30, ...}}
    ]
    """
    headers = _get_headers(config)
    url = f"{settings.FRAPPE_BASE_URL}/api/method/well_pro.well_pro_app.api.store_ai_record"
    
    if len(records) == 1 and not atomic:
        payload = {
            "domain": records[0].get("domain"),
            "record_data": records[0].get("record_data", {})
        }
    else:
        payload = {
            "atomic": atomic,
            "records": records
        }

    async with httpx.AsyncClient(timeout=10.0) as client:
        res = await client.post(url, headers=headers, json=payload)
        if res.status_code == 200:
            return json.dumps(res.json().get("message", {}), indent=2)
        return f"Error inserting record(s) ({res.status_code}): {res.text}"


@tool
async def update_user_record_tool(
    doctype: str, 
    name: str, 
    update_data: Dict[str, Any], 
    config: RunnableConfig = None
) -> str:
    """
    Update an existing Frappe record by document name/ID.
    doctype: Target DocType name (e.g. 'Health Daily Record', 'Financial Transaction')
    name: Document ID (e.g. 'FIN-TRA-2026-10-00001')
    update_data: Dictionary of fields to update.
    """
    headers = _get_headers(config)
    url = f"{settings.FRAPPE_BASE_URL}/api/method/well_pro.well_pro_app.api.update_record"
    payload = {
        "doctype": doctype,
        "name": name,
        "update_data": update_data
    }

    async with httpx.AsyncClient(timeout=10.0) as client:
        res = await client.post(url, headers=headers, json=payload)
        if res.status_code == 200:
            return json.dumps(res.json().get("message", {}), indent=2)
        return f"Error updating record ({res.status_code}): {res.text}"


@tool
async def delete_user_record_tool(
    doctype: str, 
    name: str, 
    config: RunnableConfig = None
) -> str:
    """
    Delete a user record from Frappe by document name/ID.
    """
    headers = _get_headers(config)
    url = f"{settings.FRAPPE_BASE_URL}/api/method/well_pro.well_pro_app.api.delete_record"
    payload = {
        "doctype": doctype,
        "name": name
    }

    async with httpx.AsyncClient(timeout=10.0) as client:
        res = await client.post(url, headers=headers, json=payload)
        if res.status_code == 200:
            return json.dumps(res.json().get("message", {}), indent=2)
        return f"Error deleting record ({res.status_code}): {res.text}"


@tool
async def get_dashboard_metrics_tool(as_of_date: Optional[str] = None, config: RunnableConfig = None) -> str:
    """
    Get user's complete wellbeing dashboard (scores, 7/30/90-day trends, confidences across health, financial, social, overall).
    """
    headers = _get_headers(config)
    url = f"{settings.FRAPPE_BASE_URL}/api/method/well_pro.well_pro_app.api.get_dashboard"
    params = {}
    if as_of_date:
        params["as_of_date"] = as_of_date

    async with httpx.AsyncClient(timeout=10.0) as client:
        res = await client.get(url, headers=headers, params=params)
        if res.status_code == 200:
            return json.dumps(res.json().get("message", {}).get("data", {}), indent=2)
        return f"Error fetching dashboard ({res.status_code}): {res.text}"