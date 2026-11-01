from datetime import datetime
import pytz
from typing import List, Dict, Any
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

from app.core.config import settings
from app.schemas.extraction import ExtractionResponse


"""
Constructs a LangChain structured extraction chain using ChatGoogleGenerativeAI
bound strictly to the ExtractionResponse Pydantic schema.
"""
_llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash-lite",
    google_api_key=settings.GEMINI_API_KEY,
    temperature=0.0,
)

# Force strict structured output matching ExtractionResponse
_structured_llm = _llm.with_structured_output(ExtractionResponse, method="json_schema")

_system_prompt = """
You are an AI data extraction engine for the WellPro personal health, wealth, and wellbeing tracking platform.
Your objective is to analyze user raw text, voice transcript dictations, or OCR image receipts and extract structured records for Frappe DocTypes.
CURRENT ANCHOR TIME CONTEXT:
- Current Date/Time: {current_datetime}
- User Local Timezone: {user_timezone}

Available Target DocTypes & Domain Rules:
1. "Health Daily Record" (domain: "health"):
   - record_date (YYYY-MM-DD), sleep_hours (float >= 0), sleep_quality (1-5), steps (int >= 0),
     active_minutes (int >= 0), exercise_minutes (int >= 0), exercise_intensity ("Low", "Moderate", "High"),
     water_liters (float >= 0), calories_consumed (float >= 0), protein_grams (float >= 0),
     fruit_veg_servings (float >= 0), energy_level (1-5), self_rated_health (1-5).
2. "Health Activity" (domain: "activity"):
   - activity_type ("Walking", "Running", "Cycling", "Gym", "Sports", "Other"),
     logged_at (YYYY-MM-DD HH:MM:SS), duration_minutes (float >= 0), distance_km (float >= 0),
     steps (int >= 0), calories_burned (float >= 0), intensity ("Low", "Moderate", "High").
3. "Financial Transaction" (domain: "financial"):
   - transaction_type ("Income", "Expense", "Transfer", "Investment", "Debt Payment"),
     category (e.g. "Groceries", "Dining", "Coffee & Snacks", "Salary", "Rent", "Utilities", "Shopping", "Transport"),
     amount (float > 0), transaction_date (YYYY-MM-DD), merchant_or_source (str),
     description (str), payment_method ("Cash", "Bank", "Card", "Digital Wallet", "Other"),
     essentiality ("Essential", "Discretionary", "Not Applicable").
4. "Financial Snapshot" (domain: "financial_snapshot"):
   - snapshot_date (YYYY-MM-DD), monthly_income (float), monthly_expenses (float),
     essential_monthly_expenses (float), liquid_savings (float), investment_value (float),
     emergency_fund (float), budget_amount (float), outstanding_debt (float),
     monthly_debt_payment (float), financial_stress_rating (1-5).
5. "Social Activity" (domain: "social"):
   - logged_at (YYYY-MM-DD HH:MM:SS), interaction_type ("In Person", "Call", "Video Call", "Messaging", "Group Activity", "Community Activity", "Other"),
     relationship_type ("Family", "Friend", "Partner", "Colleague", "Community", "Other"),
     duration_minutes (float >= 0), interaction_quality (1-5), connection_level (1-5), mood_after (1-5), notes (str).
6. "Subjective Wellbeing Checkin" (domain: "wellbeing"):
   - date (YYYY-MM-DD), mood (1-5), energy (1-5), stress (1-5), social_connection (1-5),
     loneliness (1-5), social_satisfaction (1-5), financial_stress (1-5).

CRITICAL VALIDATION RULES:
- Never include system fields like 'name', 'owner', 'user', 'creation', or 'docstatus'.
- Rating fields (mood, stress, quality, energy) MUST be integers between 1 and 5.
- Transaction amounts MUST be floats strictly greater than 0.
- If the user input mentions multiple distinct domains (e.g. bought food AND ran 5km), return a separate ExtractedRecord item for EACH domain.
- Currency Conversion Rule: All amounts must strictly be in PKR. If the user mentions a foreign currency (e.g., USD, EUR, GBP, AED, SAR), convert it to PKR (1 USD ≈ 278 PKR, 1 EUR ≈ 300 PKR, 1 GBP ≈ 355 PKR, 1 AED ≈ 76 PKR, 1 SAR ≈ 74 PKR) and store the final converted numeric value in amount. Note the original amount and currency in the description.
when i do some social activity and my mood details also add in the subjective wellbeing checkin.
"""

_prompt = ChatPromptTemplate.from_messages([
    ("system", _system_prompt),
    ("human", "{user_input}")
])

# Compile the Runnable Chain once as a module singleton
extraction_chain = _prompt | _structured_llm


# 1. Update the function signature to accept timezone_str
async def extract_structured_records_single_pass(raw_text: str, timezone_str: str = "Asia/Karachi") -> ExtractionResponse:
    """
    Invokes the pre-compiled singleton extraction chain directly.
    Reuses persistent HTTP connection pools and avoids per-request initialization.
    """
    try:
        user_tz = pytz.timezone(timezone_str or "Asia/Karachi")
    except Exception:
        user_tz = pytz.timezone("Asia/Karachi")
        timezone_str = "Asia/Karachi"

    now_local = datetime.now(user_tz)
    current_datetime_str = now_local.strftime("%Y-%m-%d %H:%M:%S")
    
    # 2. Add the missing time variables to the payload here
    result: ExtractionResponse = await extraction_chain.ainvoke({
        "user_input": raw_text,
        "current_datetime": current_datetime_str,
        "user_timezone": timezone_str
    })
    return result

