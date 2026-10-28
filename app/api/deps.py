from typing import Optional
import httpx
from fastapi import Header, HTTPException, status

from app.core.config import settings
from app.schemas.auth import UserSessionData, WellProProfile, UserConsentPreference


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
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not authorization.startswith("token "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Authorization header format. Expected 'token <api_key>:<api_secret>'",
        )

    frappe_verify_url = f"{settings.FRAPPE_BASE_URL}/api/method/well_pro.well_pro_app.api.verify_user_session"

    headers = {
        "Authorization": authorization,
        "Content-Type": "application/json",
    }

    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            response = await client.get(frappe_verify_url, headers=headers)
        except httpx.RequestError as exc:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Unable to reach Frappe authentication service: {str(exc)}",
            )

    if response.status_code != 200:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired Frappe session token",
        )

    res_json = response.json()
    message_wrapper = res_json.get("message", {})

    if not message_wrapper.get("success", False):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=message_wrapper.get("message", "Frappe authentication failed"),
        )

    data = message_wrapper.get("data", {})
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