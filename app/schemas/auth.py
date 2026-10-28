import json
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field, EmailStr, field_validator


class WellProProfile(BaseModel):
    name: Optional[str] = None
    user: str = Field(..., description="User email identifier from Frappe")
    date_of_birth: Optional[str] = None
    timezone: str = "UTC"
    preferred_currency: Optional[str] = None
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
    allow_ai_processing: int = 0
    allow_voice_logging: int = 0
    allow_document_ocr: int = 0
    track_social_wellbeing: int = 1
    health_tracking_enabled: int = 1
    financial_tracking_enabled: int = 1
    social_tracking_enabled: int = 1
    allow_voice_processing: int = 0
    allow_image_processing: int = 0
    allow_health_ai_processing: int = 0
    allow_financial_ai_processing: int = 0
    consent_version: str = "v1.0"


class UserSessionData(BaseModel):
    user_email: str
    profile: WellProProfile
    consent: UserConsentPreference
    raw_token: str