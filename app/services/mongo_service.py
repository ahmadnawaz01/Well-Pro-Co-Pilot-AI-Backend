from datetime import datetime
from typing import Any, Dict, List, Optional
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.schemas.auth import UserSessionData


async def log_ingestion_event(
    db: AsyncIOMotorDatabase,
    session: UserSessionData,
    raw_text: str,
    extracted_records: List[Dict[str, Any]],
    frappe_dispatch_results: List[Dict[str, Any]],
    execution_error: Optional[str] = None
) -> str:
    """
    Archives ingestion requests, extracted records, and Frappe RPC dispatch results 
    to MongoDB Atlas for audit trailing and future chatbot memory.
    """
    collection = db["ingestion_logs"]

    log_doc = {
        "user_email": session.user_email,
        "raw_text": raw_text,
        "user_profile": session.profile.model_dump(),
        "user_consent": session.consent.model_dump(),
        "extracted_records": extracted_records,
        "frappe_dispatch_results": frappe_dispatch_results,
        "execution_error": execution_error,
        "created_at": datetime.utcnow().isoformat()
    }

    result = await collection.insert_one(log_doc)
    return str(result.inserted_id)