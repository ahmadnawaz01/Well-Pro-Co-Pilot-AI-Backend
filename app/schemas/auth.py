import json
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field, EmailStr, field_validator, model_validator


class SignupRequest(BaseModel):
    email: EmailStr = Field(..., description="User's valid email address")
    password: str = Field(..., min_length=6, description="User password")
    first_name: Optional[str] = Field(None, description="First name")
    last_name: Optional[str] = Field(None, description="Last name")


class LoginRequest(BaseModel):
    usr: Optional[str] = Field(None, description="User email (Frappe username)")
    pwd: Optional[str] = Field(None, description="User password")
    email: Optional[str] = Field(None, description="User email alias")
    password: Optional[str] = Field(None, description="User password alias")

    @model_validator(mode="before")
    @classmethod
    def resolve_aliases(cls, values: Any) -> Any:
        if isinstance(values, dict):
            if not values.get("usr") and values.get("email"):
                values["usr"] = values["email"]
            if not values.get("pwd") and values.get("password"):
                values["pwd"] = values["password"]
            if not values.get("usr") or not values.get("pwd"):
                raise ValueError("Must provide usr (or email) and pwd (or password)")
        return values


class AuthTokenData(BaseModel):
    user: str = Field(..., description="User email identifier")
    api_key: str = Field(..., description="Frappe API Key")
    api_secret: str = Field(..., description="Frappe API Secret")


class AuthResponse(BaseModel):
    success: bool = True
    message: str
    data: AuthTokenData


class WellProProfile(BaseModel):
    name: Optional[str] = None
    user: str = Field(..., description="User email identifier from Frappe")
    date_of_birth: Optional[str] = None
    timezone: str = "UTC"
    preferred_currency: Optional[str] = "USD"
    height_cm: Optional[float] = None
    health_tracking_enabled: int = 1
    financial_tracking_enabled: int = 1
    social_tracking_enabled: int = 1
    custom_scoring_goals: Optional[Dict[str, Any]] = None

    @field_validator("custom_scoring_goals", mode="before")
    @classmethod
    def parse_scoring_goals_json(cls, v: Any) -> Optional[Dict[str, Any]]:
        """Parses the stringified JSON from Frappe's custom_scoring_goals field."""
        if isinstance(v, str) and v.strip():
            try:
                return json.loads(v)
            except json.JSONDecodeError:
                return {}
        return v if isinstance(v, dict) else {}


class UserConsentPreference(BaseModel):
    name: Optional[str] = None
    user: str = Field(..., description="User email identifier from Frappe")
    allow_ai_processing: int = 1
    allow_voice_logging: int = 1
    allow_document_ocr: int = 1
    track_social_wellbeing: int = 1
    health_tracking_enabled: int = 1
    financial_tracking_enabled: int = 1
    social_tracking_enabled: int = 1
    allow_voice_processing: int = 1
    allow_image_processing: int = 1
    allow_health_ai_processing: int = 1
    allow_financial_ai_processing: int = 1
    consent_version: str = "v1.0"


class UserSessionData(BaseModel):
    user_email: str
    profile: WellProProfile
    consent: UserConsentPreference
    raw_token: str


class SessionVerifyResponse(BaseModel):
    success: bool = True
    message: str = "Session valid"
    data: Dict[str, Any]
