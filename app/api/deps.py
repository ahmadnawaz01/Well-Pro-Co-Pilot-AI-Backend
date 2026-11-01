from typing import Optional
from fastapi import Header, HTTPException, status

from app.core.config import settings
from app.schemas.auth import UserSessionData, WellProProfile, UserConsentPreference
from app.services.frappe_client import FrappeClient


async def verify_frappe_token(
    authorization: Optional[str] = Header(None, alias="Authorization")
) -> UserSessionData:
    """
    FastAPI dependency that extracts the raw Authorization token header,
    verifies session validity with Frappe RPC, and returns UserSessionData.
    """
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing Authorization header",
            headers={"WWW-Authenticate": "token"},
        )

    if not authorization.startswith("token "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Authorization header format. Expected 'token <api_key>:<api_secret>'",
        )

    try:
        res = await FrappeClient.verify_user_session(token=authorization)
    except HTTPException as http_exc:
        raise http_exc
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Unable to reach Frappe authentication service: {str(exc)}",
        )

    # res can be {"success": True, "message": "...", "data": {...}} or directly data
    if isinstance(res, dict) and not res.get("success", True):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=res.get("message", "Frappe authentication failed"),
        )

    data = res.get("data", res) if isinstance(res, dict) else {}
    user_email = data.get("user")

    if not user_email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Frappe verify session payload missing 'user' email field",
        )

    profile_data = data.get("profile", {})
    consent_data = data.get("consent", {})

    # Ensure 'user' is populated inside profile and consent payloads
    profile_data["user"] = user_email
    consent_data["user"] = user_email

    return UserSessionData(
        user_email=user_email,
        profile=WellProProfile(**profile_data),
        consent=UserConsentPreference(**consent_data),
        raw_token=authorization,
    )
