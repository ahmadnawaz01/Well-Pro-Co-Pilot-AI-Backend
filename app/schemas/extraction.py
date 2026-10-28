from typing import Any, Dict, List, Literal, Optional
from pydantic import BaseModel, Field




class HealthDailyRecordSchema(BaseModel):
    record_date: str = Field(..., description="Date strictly in YYYY-MM-DD format")
    sleep_hours: Optional[float] = Field(None, ge=0.0, le=24.0)
    sleep_quality: Optional[int] = Field(None, ge=1, le=5)
    steps: Optional[int] = Field(None, ge=0)
    active_minutes: Optional[int] = Field(None, ge=0)
    exercise_minutes: Optional[int] = Field(None, ge=0)
    exercise_intensity: Optional[Literal["Low", "Moderate", "High"]] = None
    water_liters: Optional[float] = Field(None, ge=0.0)
    calories_consumed: Optional[float] = Field(None, ge=0.0)
    protein_grams: Optional[float] = Field(None, ge=0.0)
    fruit_veg_servings: Optional[float] = Field(None, ge=0.0)
    energy_level: Optional[int] = Field(None, ge=1, le=5)
    self_rated_health: Optional[int] = Field(None, ge=1, le=5)
    source: str = Field("AI Extraction", description="Data origin")


class HealthActivitySchema(BaseModel):
    activity_type: Literal["Walking", "Running", "Cycling", "Gym", "Sports", "Other"]
    logged_at: str = Field(..., description="Timestamp strictly in YYYY-MM-DD HH:MM:SS format")
    duration_minutes: Optional[float] = Field(None, ge=0.0)
    distance_km: Optional[float] = Field(None, ge=0.0)
    steps: Optional[int] = Field(None, ge=0)
    calories_burned: Optional[float] = Field(None, ge=0.0)
    intensity: Optional[Literal["Low", "Moderate", "High"]] = None
    source: str = Field("AI Extraction")


class FinancialTransactionSchema(BaseModel):
    transaction_type: Literal["Income", "Expense", "Transfer", "Investment", "Debt Payment"]
    category: str = Field(..., description="Must link to a valid Financial Category string")
    amount: float = Field(..., gt=0.0, description="Monetary value strictly greater than 0")
    transaction_date: str = Field(..., description="Date strictly in YYYY-MM-DD format")
    merchant_or_source: Optional[str] = None
    description: Optional[str] = None
    payment_method: Optional[Literal["Cash", "Bank", "Card", "Digital Wallet", "Other"]] = None
    is_recurring: int = Field(0, ge=0, le=1)
    essentiality: Literal["Essential", "Discretionary", "Not Applicable"] = "Discretionary"
    source: str = Field("AI Extraction")


class SocialActivitySchema(BaseModel):
    logged_at: str = Field(..., description="Timestamp strictly in YYYY-MM-DD HH:MM:SS format")
    interaction_type: Literal["In Person", "Call", "Video Call", "Messaging", "Group Activity", "Community Activity", "Other"]
    relationship_type: Literal["Family", "Friend", "Partner", "Colleague", "Community", "Other"]
    duration_minutes: Optional[float] = Field(None, ge=0.0)
    interaction_quality: Optional[int] = Field(None, ge=1, le=5)
    connection_level: Optional[int] = Field(None, ge=1, le=5)
    mood_after: Optional[int] = Field(None, ge=1, le=5)
    notes: Optional[str] = None
    source: str = Field("AI Extraction")


class SubjectiveWellbeingCheckinSchema(BaseModel):
    date: str = Field(..., description="Date strictly in YYYY-MM-DD format")
    mood: Optional[int] = Field(None, ge=1, le=5)
    energy: Optional[int] = Field(None, ge=1, le=5)
    stress: Optional[int] = Field(None, ge=1, le=5)
    social_connection: Optional[int] = Field(None, ge=1, le=5)
    loneliness: Optional[int] = Field(None, ge=1, le=5)
    social_satisfaction: Optional[int] = Field(None, ge=1, le=5)
    financial_stress: Optional[int] = Field(None, ge=1, le=5)




AllowedDocType = Literal[
    "Health Daily Record",
    "Health Activity",
    "Financial Transaction",
    "Financial Snapshot",
    "Social Activity",
    "Subjective Wellbeing Checkin",
]

AllowedDomain = Literal["health", "health_activity", "financial", "social", "wellbeing"]


class ExtractedRecord(BaseModel):
    doctype: str = Field(description="Target Frappe DocType name")
    domain: str = Field(description="Domain category (health, health_activity, financial, social, wellbeing)")
    record_data: Dict[str, Any] = Field(description="Key-value dictionary conforming to DocType schema")


class ExtractionResponse(BaseModel):
    is_relevant: bool = Field(
        ..., 
        description="True if input contains actionable health, activity, financial, social, or wellbeing data."
    )
    relevance_reason: Optional[str] = Field(
        None, 
        description="Brief reason if input is off-topic or relevant."
    )
    records: List[ExtractedRecord] = Field(
        default_factory=list, 
        description="Extracted domain records."
    )