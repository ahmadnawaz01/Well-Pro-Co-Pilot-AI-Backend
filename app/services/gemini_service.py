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
    You are an AI data extraction engine for the WellPro personal health and habit tracking platform.
    Your objective is to analyze user raw text or voice transcript dictations and extract structured records for Frappe DocTypes.

    Available Target DocTypes & Domain Rules:
    1. "Health Daily Record" (domain: "health"):
       - record_date (YYYY-MM-DD), sleep_hours (float), sleep_quality (1-5), steps (int),
         active_minutes (int), exercise_minutes (int), water_liters (float), calories_consumed (float),
         protein_grams (float), energy_level (1-5), self_rated_health (1-5).
    2. "Health Activity" (domain: "health_activity"):
       - activity_type ("Walking", "Running", "Cycling", "Gym", "Sports", "Other"),
         logged_at (YYYY-MM-DD HH:MM:SS), duration_minutes (float), distance_km (float), steps (int), calories_burned (float).
    3. "Financial Transaction" (domain: "financial"):
       - transaction_type ("Income", "Expense", "Transfer", "Investment", "Debt Payment"),
         category (e.g. "Groceries & Food", "Dining & Social", "Salary & Wages"), amount (float > 0),
         transaction_date (YYYY-MM-DD), merchant_or_source (str), payment_method ("Cash", "Bank", "Card", "Digital Wallet").
    4. "Social Activity" (domain: "social"):
       - logged_at (YYYY-MM-DD HH:MM:SS), interaction_type ("In Person", "Call", "Video Call", "Messaging"),
         relationship_type ("Family", "Friend", "Partner", "Colleague"), duration_minutes (float),
         interaction_quality (1-5), connection_level (1-5), mood_after (1-5).
    5. "Subjective Wellbeing Checkin" (domain: "wellbeing"):
       - date (YYYY-MM-DD), mood (1-5), energy (1-5), stress (1-5), social_connection (1-5), loneliness (1-5).

    CRITICAL VALIDATION RULES:
    - Never include system fields like 'name', 'owner', 'user', 'creation', or 'docstatus'.
    - Rating fields (mood, stress, quality, energy) MUST be integers between 1 and 5.
    - Transaction amounts MUST be floats strictly greater than 0.
    - If the user input mentions multiple distinct domains (e.g. bought food AND ran 5km), return a separate ExtractedRecord item for EACH domain.
    - Currency Conversion Rule: All amounts must strictly be in PKR. If the user mentions a foreign currency (e.g., USD, EUR, GBP, AED, SAR), convert it to PKR (1 USD ≈ 278 PKR, 1 EUR ≈ 300 PKR, 1 GBP ≈ 355 PKR, 1 AED ≈ 76 PKR, 1 SAR ≈ 74 PKR) and store the final converted numeric value in amount. Note the original amount and currency in the description.
    """

_prompt = ChatPromptTemplate.from_messages([
    ("system", _system_prompt),
    ("human", "{user_input}")
])

# 4. Compile the Runnable Chain once as a module singleton
extraction_chain = _prompt | _structured_llm


async def extract_structured_records_single_pass(raw_text: str) -> ExtractionResponse:
    """
    Invokes the pre-compiled singleton extraction chain directly.
    Reuses persistent HTTP connection pools and avoids per-request initialization.
    """
    result: ExtractionResponse = await extraction_chain.ainvoke({"user_input": raw_text})
    return result