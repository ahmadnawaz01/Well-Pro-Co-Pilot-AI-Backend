from typing import Any, Dict, Optional
from fastapi import APIRouter, Depends, Query, status, Body

from app.api.deps import verify_frappe_token
from app.schemas.auth import UserSessionData
from app.schemas.dashboard import RecalculateScoreRequest
from app.services.frappe_client import FrappeClient

router = APIRouter()


@router.get(
    "/metrics",
    status_code=status.HTTP_200_OK,
    summary="Get Dashboard Metrics (GET)",
    description="Primary dashboard analytics endpoint. Computes current scores, multi-window recency-weighted summaries (7d, 30d, 90d), historical score timelines, and recent domain feeds."
)
async def get_dashboard_metrics_get(
    days: int = Query(30, ge=1, le=365, description="Lookback window in days for historical timeline"),
    as_of_date: Optional[str] = Query(None, description="Evaluation target date (YYYY-MM-DD, defaults to today)"),
    session: UserSessionData = Depends(verify_frappe_token),
):
    result = await FrappeClient.get_dashboard_metrics(
        token=session.raw_token,
        days=days,
        as_of_date=as_of_date,
    )
    return result


@router.post(
    "/metrics",
    status_code=status.HTTP_200_OK,
    summary="Get Dashboard Metrics (POST)",
    description="Primary dashboard analytics endpoint (POST compatibility). Accepts JSON payload with 'days' and 'as_of_date'."
)
async def get_dashboard_metrics_post(
    days: int = Body(30, embed=True, ge=1, le=365, description="Lookback window in days for historical timeline"),
    as_of_date: Optional[str] = Body(None, embed=True, description="Evaluation target date (YYYY-MM-DD)"),
    session: UserSessionData = Depends(verify_frappe_token),
):
    result = await FrappeClient.get_dashboard_metrics(
        token=session.raw_token,
        days=days,
        as_of_date=as_of_date,
    )
    return result


@router.post(
    "/recalculate-score",
    status_code=status.HTTP_200_OK,
    summary="Recalculate Wellbeing Score",
    description="Explicitly forces daily score recalculation for a specified date (YYYY-MM-DD). If omitted, recalculates today's scores."
)
async def recalculate_score(
    payload: Optional[RecalculateScoreRequest] = None,
    session: UserSessionData = Depends(verify_frappe_token),
):
    target_date = payload.date if payload else None
    result = await FrappeClient.recalculate_score(date=target_date, token=session.raw_token)
    return result

