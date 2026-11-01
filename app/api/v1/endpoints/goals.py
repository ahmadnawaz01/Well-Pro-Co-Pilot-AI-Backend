from typing import Any, Dict, Optional
from fastapi import APIRouter, Depends, status

from app.api.deps import verify_frappe_token
from app.schemas.auth import UserSessionData
from app.schemas.goals import SetupGoalsRequest
from app.services.frappe_client import FrappeClient

router = APIRouter()


@router.post(
    "/setup",
    status_code=status.HTTP_200_OK,
    summary="Setup Scoring Goals",
    description="Configures custom scoring goals. Parses human-friendly strings (e.g. '12k', '$3,500', '25%', '3L') into standardized targets and optionally recalculates scores."
)
async def setup_scoring_goals(
    payload: SetupGoalsRequest,
    session: UserSessionData = Depends(verify_frappe_token),
):
    result = await FrappeClient.setup_scoring_goals(
        goals=payload.goals,
        recalculate=payload.recalculate,
        token=session.raw_token,
    )
    return result


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    summary="Get Scoring Goals (GET)",
    description="Retrieves current active scoring goals for the authenticated user, merged with system baseline targets."
)
async def get_scoring_goals_get(
    session: UserSessionData = Depends(verify_frappe_token),
):
    result = await FrappeClient.get_scoring_goals(token=session.raw_token)
    return result


@router.post(
    "",
    status_code=status.HTTP_200_OK,
    summary="Get Scoring Goals (POST)",
    description="Retrieves current active scoring goals (POST compatibility)."
)
async def get_scoring_goals_post(
    session: UserSessionData = Depends(verify_frappe_token),
):
    result = await FrappeClient.get_scoring_goals(token=session.raw_token)
    return result

