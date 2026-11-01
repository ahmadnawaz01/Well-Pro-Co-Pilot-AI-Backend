import json
from typing import Optional, Dict, Any, List
from langchain_core.tools import tool
from langchain_core.runnables import RunnableConfig

from app.services.frappe_client import FrappeClient
from app.services.frappe_dispatch import build_store_ai_payload


def _get_token(config: RunnableConfig) -> str:
    """Retrieves caller's Frappe token from LangGraph runtime config context."""
    token = config.get("configurable", {}).get("frappe_token")
    if not token:
        raise ValueError("Authentication token missing from session context.")
    return token


@tool
async def get_user_records_tool(
    doctype: str, 
    from_date: Optional[str] = None, 
    to_date: Optional[str] = None, 
    limit: int = 20, 
    offset: int = 0,
    order_by: Optional[str] = None,
    config: RunnableConfig = None
) -> str:
    """
    Fetch user records from Frappe for question-answering, auditing, or viewing history.
    doctype: Allowed DocTypes: 'Health Daily Record', 'Health Activity', 'Financial Transaction', 
             'Financial Snapshot', 'Social Activity', 'Subjective Wellbeing Checkin'.
    from_date / to_date: Optional YYYY-MM-DD string filters.
    limit: Number of records to retrieve (default 20, max 200).
    offset: Pagination offset.
    order_by: e.g. 'transaction_date desc', 'record_date desc', 'creation desc'.
    """
    token = _get_token(config)
    try:
        data = await FrappeClient.get_user_records(
            doctype=doctype,
            token=token,
            limit=limit,
            offset=offset,
            order_by=order_by,
            from_date=from_date,
            to_date=to_date,
        )
        return json.dumps(data, indent=2)
    except Exception as exc:
        return f"Error fetching records: {str(exc)}"


@tool
async def insert_user_records_tool(
    records: List[Dict[str, Any]], 
    config: RunnableConfig = None
) -> str:
    """
    Insert single or batch records into Frappe using the v2.0.0 store_ai_record endpoint.
    records: List of dicts, each with keys 'domain' ('health', 'health_activity', 'activity', 'financial', 'financial_snapshot', 'social', 'wellbeing')
             and 'record_data' dict conforming to the DocType schema.
    Example:
    records = [
      {"domain": "financial", "record_data": {"transaction_type": "Expense", "amount": 12.0, "category": "Lunch"}},
      {"domain": "health", "record_data": {"record_date": "2026-10-30", "steps": 8500, "sleep_hours": 7.5}}
    ]
    """
    token = _get_token(config)
    try:
        payload = build_store_ai_payload(records)
        res = await FrappeClient.store_ai_record(payload=payload, token=token)
        return json.dumps(res, indent=2)
    except Exception as exc:
        return f"Error inserting record(s): {str(exc)}"


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
    name: Document ID (e.g. 'FT-00109' or 'HDR-00042')
    update_data: Dictionary of fields to update.
    """
    token = _get_token(config)
    try:
        res = await FrappeClient.update_record(
            doctype=doctype,
            name=name,
            update_data=update_data,
            token=token,
        )
        return json.dumps(res, indent=2)
    except Exception as exc:
        return f"Error updating record: {str(exc)}"


@tool
async def delete_user_record_tool(
    doctype: str, 
    name: str, 
    config: RunnableConfig = None
) -> str:
    """
    Delete a user record from Frappe by document name/ID.
    doctype: Target DocType name.
    name: Target document ID (e.g. 'FT-00109').
    """
    token = _get_token(config)
    try:
        res = await FrappeClient.delete_record(
            doctype=doctype,
            name=name,
            token=token,
        )
        return json.dumps(res, indent=2)
    except Exception as exc:
        return f"Error deleting record: {str(exc)}"


@tool
async def get_dashboard_metrics_tool(
    days: int = 30,
    as_of_date: Optional[str] = None, 
    config: RunnableConfig = None
) -> str:
    """
    Get user's complete wellbeing dashboard:
    - Current scores (health, financial, social, overall, confidence).
    - Multi-window rolling summaries (7-day, 30-day, 90-day recency-weighted scores and trends).
    - Historical trend timeline.
    - Recent feeds across health, financial transactions, social logs, and checkins.
    """
    token = _get_token(config)
    try:
        res = await FrappeClient.get_dashboard_metrics(
            token=token,
            days=days,
            as_of_date=as_of_date,
        )
        return json.dumps(res, indent=2)
    except Exception as exc:
        return f"Error fetching dashboard metrics: {str(exc)}"


@tool
async def recalculate_score_tool(
    date: Optional[str] = None,
    config: RunnableConfig = None
) -> str:
    """
    Explicitly triggers recalculation of wellbeing daily scores for a specific date (YYYY-MM-DD).
    If date is omitted, defaults to today.
    """
    token = _get_token(config)
    try:
        res = await FrappeClient.recalculate_score(date=date, token=token)
        return json.dumps(res, indent=2)
    except Exception as exc:
        return f"Error recalculating score: {str(exc)}"


@tool
async def setup_scoring_goals_tool(
    goals: Dict[str, Any],
    recalculate: bool = True,
    config: RunnableConfig = None
) -> str:
    """
    Configure personal wellbeing scoring targets in Frappe.
    Accepts human-friendly string values:
    e.g. {"steps": "10k", "financial_budget": "$3,000", "savings_rate": "20%", "water": "3L", "exercise_minutes": 45}
    recalculate: Whether to automatically recalculate current scores with the new goals.
    """
    token = _get_token(config)
    try:
        res = await FrappeClient.setup_scoring_goals(goals=goals, recalculate=recalculate, token=token)
        return json.dumps(res, indent=2)
    except Exception as exc:
        return f"Error setting up scoring goals: {str(exc)}"


@tool
async def get_scoring_goals_tool(config: RunnableConfig = None) -> str:
    """
    Retrieve user's active scoring goals merged with system baseline targets.
    """
    token = _get_token(config)
    try:
        res = await FrappeClient.get_scoring_goals(token=token)
        return json.dumps(res, indent=2)
    except Exception as exc:
        return f"Error retrieving scoring goals: {str(exc)}"
