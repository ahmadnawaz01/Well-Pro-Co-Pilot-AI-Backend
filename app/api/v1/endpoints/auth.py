from fastapi import APIRouter, Depends, Header, status
from typing import Optional

from app.schemas.auth import (
    SignupRequest,
    LoginRequest,
    AuthResponse,
    SessionVerifyResponse,
    UserSessionData,
)
from app.api.deps import verify_frappe_token
from app.services.frappe_client import FrappeClient

router = APIRouter()


@router.post(
    "/signup",
    response_model=AuthResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register New User",
    description="Registers a new user in Frappe, generates API key and secret credentials, and initializes WellPro Profile and Consent models."
)
async def signup(payload: SignupRequest):
    result = await FrappeClient.signup(
        email=str(payload.email),
        password=payload.password,
        first_name=payload.first_name,
        last_name=payload.last_name,
    )

    data = result.get("data", result)
    message = result.get("message", "User registered successfully") if isinstance(result, dict) else "User registered successfully"

    return AuthResponse(
        success=True,
        message=message if isinstance(message, str) else "User registered successfully",
        data=data,
    )


@router.post(
    "/login",
    response_model=AuthResponse,
    status_code=status.HTTP_200_OK,
    summary="User Login",
    description="Authenticates credentials against Frappe backend and returns user API key and secret."
)
async def login(payload: LoginRequest):
    result = await FrappeClient.login(
        usr=payload.usr or payload.email,
        pwd=payload.pwd or payload.password,
    )

    data = result.get("data", result)
    message = result.get("message", "Authentication successful") if isinstance(result, dict) else "Authentication successful"

    return AuthResponse(
        success=True,
        message=message if isinstance(message, str) else "Authentication successful",
        data=data,
    )


@router.get(
    "/verify-session",
    response_model=SessionVerifyResponse,
    status_code=status.HTTP_200_OK,
    summary="Verify User Session (GET)",
    description="Validates API credentials in Authorization header and returns user profile and consent settings."
)
async def verify_session_get(session: UserSessionData = Depends(verify_frappe_token)):
    return SessionVerifyResponse(
        success=True,
        message="Session valid",
        data={
            "user": session.user_email,
            "profile": session.profile.model_dump(),
            "consent": session.consent.model_dump(),
        }
    )


@router.post(
    "/verify-session",
    response_model=SessionVerifyResponse,
    status_code=status.HTTP_200_OK,
    summary="Verify User Session (POST)",
    description="Validates API credentials in Authorization header and returns user profile and consent settings (Frappe POST compatibility)."
)
async def verify_session_post(session: UserSessionData = Depends(verify_frappe_token)):
    return SessionVerifyResponse(
        success=True,
        message="Session valid",
        data={
            "user": session.user_email,
            "profile": session.profile.model_dump(),
            "consent": session.consent.model_dump(),
        }
    )

