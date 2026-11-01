import json
from typing import List, Dict, Any
from pymongo import MongoClient
from langgraph.checkpoint.mongodb import MongoDBSaver
from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI

from app.core.config import settings
from app.tools.frappe_tools import (
    get_user_records_tool,
    insert_user_records_tool,
    update_user_record_tool,
    delete_user_record_tool,
    get_dashboard_metrics_tool,
    recalculate_score_tool,
    setup_scoring_goals_tool,
    get_scoring_goals_tool,
)


_mongo_client = MongoClient(settings.MONGODB_URL)
checkpointer = MongoDBSaver(
    client=_mongo_client,
    db_name=settings.MONGODB_DB_NAME,
    checkpoint_collection_name="chat_checkpoints",
    writes_collection_name="chat_writes"
)


chatbot_tools = [
    get_user_records_tool,
    insert_user_records_tool,
    update_user_record_tool,
    delete_user_record_tool,
    get_dashboard_metrics_tool,
    recalculate_score_tool,
    setup_scoring_goals_tool,
    get_scoring_goals_tool,
]

# 3. LLM Setup
_llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash-lite",
    google_api_key=settings.GEMINI_API_KEY,
    temperature=0.2,
)

# 4. System Prompt
system_prompt = """
You are WellPro Co-Pilot, an intelligent personal health, wealth, social, and wellbeing assistant.
You have access to tools that query, create, batch insert, update, delete user records, inspect dashboard analytics, recalculate scores, and configure scoring targets in Frappe.

Available Target DocTypes & Domain Rules:
    1. "Health Daily Record" (domain: "health"):
       - record_date (YYYY-MM-DD), sleep_hours (float >= 0), sleep_quality (1-5), steps (int >= 0),
         active_minutes (int >= 0), exercise_minutes (int >= 0), water_liters (float >= 0),
         calories_consumed (float >= 0), protein_grams (float >= 0), fruit_veg_servings (float >= 0),
         energy_level (1-5), self_rated_health (1-5).
    2. "Health Activity" (domain: "activity"):
       - activity_type ("Walking", "Running", "Cycling", "Gym", "Sports", "Other"),
         logged_at (YYYY-MM-DD HH:MM:SS), duration_minutes (float >= 0), distance_km (float >= 0),
         steps (int >= 0), calories_burned (float >= 0), intensity ("Low", "Moderate", "High").
    3. "Financial Transaction" (domain: "financial"):
       - transaction_type ("Income", "Expense", "Transfer", "Investment", "Debt Payment"),
         category (e.g. "Groceries", "Dining", "Salary", "Rent", "Utilities"), amount (float > 0),
         transaction_date (YYYY-MM-DD), merchant_or_source (str), payment_method ("Cash", "Bank", "Card", "Digital Wallet", "Other"),
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
- Currency Conversion Rule: All amounts must strictly be in PKR. If the user mentions a foreign currency (e.g., USD, EUR, GBP, AED, SAR), convert it to PKR (1 USD ≈ 278 PKR, 1 EUR ≈ 300 PKR, 1 GBP ≈ 355 PKR, 1 AED ≈ 76 PKR, 1 SAR ≈ 74 PKR) and store the final converted numeric value in amount. Note the original amount and currency in the description.

Instructions:
1. When asked to log or insert data, use `insert_user_records_tool` which supports multi-document extraction and batch insertion.
2. When asked questions about the user's progress or history, use `get_user_records_tool` or `get_dashboard_metrics_tool`.
3. When asked to view or update wellbeing targets (e.g. 10,000 steps, $2,000 budget), use `get_scoring_goals_tool` and `setup_scoring_goals_tool`.
4. When asked to recalculate scores for a date, use `recalculate_score_tool`.
5. Always ask for explicit confirmation before calling `delete_user_record_tool`.
6. Maintain a helpful, empathetic, concise, and motivating tone.
"""

# 5. Compiled ReAct Agent
chatbot_agent = create_agent(
    model=_llm,
    tools=chatbot_tools,
    system_prompt=system_prompt,
    checkpointer=checkpointer
)


async def execute_chat_message(
    user_email: str,
    raw_token: str,
    message: str,
    session_id: str = "default"
) -> str:
    """Executes a chat step within a user-isolated thread ID namespace."""
    thread_id = f"{user_email}:{session_id}"
    config = {
        "configurable": {
            "thread_id": thread_id,
            "frappe_token": raw_token
        }
    }

    input_payload = {"messages": [("user", message)]}
    final_state = await chatbot_agent.ainvoke(input_payload, config=config)

    # Extract last message
    last_message = final_state["messages"][-1]
    raw_content = last_message.content

    # Handle string vs list[dict] Gemini block content formats
    if isinstance(raw_content, str):
        return raw_content
    elif isinstance(raw_content, list):
        text_parts = []
        for block in raw_content:
            if isinstance(block, dict) and block.get("type") == "text":
                text_parts.append(block.get("text", ""))
            elif isinstance(block, str):
                text_parts.append(block)
        return "\n".join(text_parts) if text_parts else str(raw_content)

    return str(raw_content)


async def fetch_user_chat_history(user_email: str, session_id: str = "default") -> List[Dict[str, Any]]:
    """
    Retrieves full chat history from MongoDB checkpointer for frontend UI rehydration.
    Safely parses both HumanMessage and AIMessage objects (including multi-block responses).
    """
    thread_id = f"{user_email}:{session_id}"
    config = {"configurable": {"thread_id": thread_id}}

    state_snapshot = await chatbot_agent.aget_state(config)
    if not state_snapshot or not state_snapshot.values:
        return []

    messages = state_snapshot.values.get("messages", [])
    history = []

    for msg in messages:
        msg_type = getattr(msg, "type", "")

        # Only process Human and AI messages (ignore raw ToolMessages)
        if msg_type in ("human", "ai"):
            # Skip AIMessage objects that are JUST tool call requests without text
            if msg_type == "ai" and getattr(msg, "tool_calls", None) and not msg.content:
                continue

            raw_content = msg.content
            text_content = ""

            # Case A: Plain String content
            if isinstance(raw_content, str):
                text_content = raw_content

            # Case B: Gemini List/Block content format (e.g. [{'type': 'text', 'text': '...'}])
            elif isinstance(raw_content, list):
                parts = []
                for block in raw_content:
                    if isinstance(block, dict) and block.get("type") == "text":
                        parts.append(block.get("text", ""))
                    elif isinstance(block, str):
                        parts.append(block)
                text_content = "\n".join(parts)

            # Only append if there is actual text content
            if text_content.strip():
                history.append({
                    "role": "user" if msg_type == "human" else "assistant",
                    "content": text_content.strip()
                })

    return history


async def clear_user_chat_history(user_email: str, session_id: str = "default") -> bool:
    """Clears checkpoint collections for given user thread."""
    thread_id = f"{user_email}:{session_id}"
    db = _mongo_client[settings.MONGODB_DB_NAME]
    
    # Delete state checkpoints matching thread_id
    db["chat_checkpoints"].delete_many({"thread_id": thread_id})
    db["chat_writes"].delete_many({"thread_id": thread_id})
    return True
