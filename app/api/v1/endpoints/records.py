from typing import Any, Dict, List, Optional, Union
from fastapi import APIRouter, Depends, Query, status, Body

from app.api.deps import verify_frappe_token
from app.schemas.auth import UserSessionData
from app.schemas.records import (
    UpdateRecordRequest,
    DeleteRecordRequest,
    GetUserRecordsQuery,
)
from app.services.frappe_client import FrappeClient

router = APIRouter()


@router.post(
    "/insert",
    status_code=status.HTTP_200_OK,
    summary="Insert Record(s) - Universal Ingestion",
    description="Universal ingestion endpoint supporting: 1. Multi-DocType payload keyed by DocType/domain; 2. Single nested/flat record; 3. Batch records array. Automatically triggers daily score recalculation and returns newly recalculated scores."
)
async def insert_record(
    payload: Union[Dict[str, Any], List[Dict[str, Any]]] = Body(
        ...,
        description="Multi-DocType object, single record dict, or batch array"
    ),
    session: UserSessionData = Depends(verify_frappe_token),
):
    result = await FrappeClient.insert_record(payload=payload, token=session.raw_token)
    return result


@router.post(
    "/store-ai",
    status_code=status.HTTP_200_OK,
    summary="Store AI Extracted Records",
    description="Dedicated endpoint for AI/Voice/OCR domain extractions (health, financial, social, wellbeing, activity). Automatically sets provenance to 'AI Extraction' and calculates daily wellbeing scores."
)
async def store_ai_record(
    payload: Dict[str, Any] = Body(
        ...,
        description="Domain-keyed extractions: {'health': {...}, 'financial': [...], 'social': {...}, 'wellbeing': {...}, 'activity': {...}}"
    ),
    session: UserSessionData = Depends(verify_frappe_token),
):
    result = await FrappeClient.store_ai_record(payload=payload, token=session.raw_token)
    return result


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    summary="Query User Records (GET)",
    description="Retrieves paginated records for a specific DocType owned by the authenticated caller."
)
async def get_user_records_get(
    doctype: str = Query(..., description="DocType name (e.g. 'Financial Transaction', 'Health Daily Record')"),
    limit: int = Query(50, ge=1, le=200, description="Max items to return"),
    offset: int = Query(0, ge=0, description="Pagination offset"),
    order_by: Optional[str] = Query(None, description="Order criteria (e.g. 'transaction_date desc')"),
    from_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    to_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
    session: UserSessionData = Depends(verify_frappe_token),
):
    result = await FrappeClient.get_user_records(
        doctype=doctype,
        token=session.raw_token,
        limit=limit,
        offset=offset,
        order_by=order_by,
        from_date=from_date,
        to_date=to_date,
    )
    return result


@router.post(
    "/query",
    status_code=status.HTTP_200_OK,
    summary="Query User Records (POST)",
    description="Retrieves paginated records for a specific DocType via JSON body payload."
)
async def get_user_records_post(
    payload: GetUserRecordsQuery,
    session: UserSessionData = Depends(verify_frappe_token),
):
    result = await FrappeClient.get_user_records(
        doctype=payload.doctype,
        token=session.raw_token,
        limit=payload.limit,
        offset=payload.offset,
        order_by=payload.order_by,
        from_date=payload.from_date,
        to_date=payload.to_date,
    )
    return result


@router.post(
    "/update",
    status_code=status.HTTP_200_OK,
    summary="Update Record (POST)",
    description="Safely updates an existing user document. Recalculates scores for the original and new dates if date fields were modified."
)
async def update_record_post(
    payload: UpdateRecordRequest,
    session: UserSessionData = Depends(verify_frappe_token),
):
    result = await FrappeClient.update_record(
        doctype=payload.doctype,
        name=payload.name,
        update_data=payload.update_data,
        token=session.raw_token,
    )
    return result


@router.put(
    "/update",
    status_code=status.HTTP_200_OK,
    summary="Update Record (PUT)",
    description="Safely updates an existing user document (RESTful PUT alias)."
)
async def update_record_put(
    payload: UpdateRecordRequest,
    session: UserSessionData = Depends(verify_frappe_token),
):
    result = await FrappeClient.update_record(
        doctype=payload.doctype,
        name=payload.name,
        update_data=payload.update_data,
        token=session.raw_token,
    )
    return result


@router.post(
    "/delete",
    status_code=status.HTTP_200_OK,
    summary="Delete Record (POST)",
    description="Safely deletes a record owned by the authenticated caller and triggers score recalculation."
)
async def delete_record_post(
    payload: DeleteRecordRequest,
    session: UserSessionData = Depends(verify_frappe_token),
):
    result = await FrappeClient.delete_record(
        doctype=payload.doctype,
        name=payload.name,
        token=session.raw_token,
    )
    return result


@router.delete(
    "/delete",
    status_code=status.HTTP_200_OK,
    summary="Delete Record (DELETE)",
    description="Safely deletes a record owned by the authenticated caller (RESTful DELETE alias)."
)
async def delete_record_delete(
    payload: DeleteRecordRequest,
    session: UserSessionData = Depends(verify_frappe_token),
):
    result = await FrappeClient.delete_record(
        doctype=payload.doctype,
        name=payload.name,
        token=session.raw_token,
    )
    return result

