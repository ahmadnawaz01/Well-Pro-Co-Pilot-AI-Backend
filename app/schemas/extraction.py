from typing import Any, Dict, List, Literal, Optional
from pydantic import BaseModel, Field


class HealthDailyRecordSchema(BaseModel):
    record_date: str = Field(..., description="Date strictly in YYYY-MM-DD format")
    sleep_hours: Optional[float] = Field(None, ge=0.0, le=24.0, description="Total sleep hours")
    sleep_quality: Optional[int] = Field(None, ge=1, le=5, description="Sleep quality rating (1-5)")
    steps: Optional[int] = Field(None, ge=0, description="Step count")
    active_minutes: Optional[int] = Field(None, ge=0, description="Active minutes")
    exercise_minutes: Optional[int] = Field(None, ge=0, description="Exercise minutes")
    exercise_intensity: Optional[Literal["Low", "Moderate", "High"]] = None
    water_liters: Optional[float] = Field(None, ge=0.0, description="Water intake in liters")
    calories_consumed: Optional[float] = Field(None, ge=0.0, description="Daily calories consumed")
    protein_grams: Optional[float] = Field(None, ge=0.0, description="Protein intake in grams")
    fruit_veg_servings: Optional[float] = Field(None, ge=0.0, description="Fruit/veg servings")
    energy_level: Optional[int] = Field(None, ge=1, le=5, description="Subjective energy rating (1-5)")
    self_rated_health: Optional[int] = Field(None, ge=1, le=5, description="General health rating (1-5)")
    source: str = Field("AI Extraction", description="Data provenance")


class HealthActivitySchema(BaseModel):
    activity_type: Literal["Walking", "Running", "Cycling", "Gym", "Sports", "Other"] = Field("Other")
    logged_at: str = Field(..., description="Timestamp strictly in YYYY-MM-DD HH:MM:SS format")
    duration_minutes: Optional[float] = Field(None, ge=0.0, description="Duration in minutes")
    distance_km: Optional[float] = Field(None, ge=0.0, description="Distance in kilometers")
    steps: Optional[int] = Field(None, ge=0, description="Activity step count")
    calories_burned: Optional[float] = Field(None, ge=0.0, description="Active calories burned")
    intensity: Optional[Literal["Low", "Moderate", "High"]] = None
    source: str = Field("AI Extraction")
    raw_input: Optional[str] = None


class FinancialTransactionSchema(BaseModel):
    transaction_type: Literal["Income", "Expense", "Transfer", "Investment", "Debt Payment"] = Field("Expense")
    category: str = Field(..., description="Financial Category name")
    amount: float = Field(..., gt=0.0, description="Monetary value strictly greater than 0")
    currency: Optional[str] = Field("PKR", description="Currency ISO code")
    transaction_date: str = Field(..., description="Date strictly in YYYY-MM-DD format")
    merchant_or_source: Optional[str] = None
    description: Optional[str] = None
    payment_method: Optional[Literal["Cash", "Bank", "Card", "Digital Wallet", "Other"]] = None
    is_recurring: int = Field(0, ge=0, le=1)
    essentiality: Literal["Essential", "Discretionary", "Not Applicable"] = "Discretionary"
    source: str = Field("AI Extraction")
    raw_input: Optional[str] = None


class FinancialSnapshotSchema(BaseModel):
    snapshot_date: str = Field(..., description="Date strictly in YYYY-MM-DD format")
    monthly_income: Optional[float] = Field(None, ge=0.0)
    monthly_expenses: Optional[float] = Field(None, ge=0.0)
    essential_monthly_expenses: Optional[float] = Field(None, ge=0.0)
    liquid_savings: Optional[float] = Field(None, ge=0.0)
    investment_value: Optional[float] = Field(None, ge=0.0)
    emergency_fund: Optional[float] = Field(None, ge=0.0)
    budget_amount: Optional[float] = Field(None, ge=0.0)
    outstanding_debt: Optional[float] = Field(None, ge=0.0)
    monthly_debt_payment: Optional[float] = Field(None, ge=0.0)
    financial_stress_rating: Optional[int] = Field(None, ge=1, le=5)
    source: str = Field("AI Extraction")


class SocialActivitySchema(BaseModel):
    logged_at: str = Field(..., description="Timestamp strictly in YYYY-MM-DD HH:MM:SS format")
    interaction_type: Literal["In Person", "Call", "Video Call", "Messaging", "Group Activity", "Community Activity", "Other"] = Field("In Person")
    relationship_type: Literal["Family", "Friend", "Partner", "Colleague", "Community", "Other"] = Field("Friend")
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

AllowedDomain = Literal[
    "health",
    "health_activity",
    "activity",
    "financial",
    "financial_snapshot",
    "social",
    "wellbeing",
]


class ExtractedRecord(BaseModel):
    doctype: str = Field(description="Target Frappe DocType name")
    domain: str = Field(description="Domain category (health, health_activity, financial, financial_snapshot, social, wellbeing)")
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
