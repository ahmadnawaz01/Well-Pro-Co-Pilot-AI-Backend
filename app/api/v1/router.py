from fastapi import APIRouter
from app.api.v1.endpoints import (
    auth,
    records,
    dashboard,
    goals,
    ingest,
    chat,
)

api_router = APIRouter()

# 5.1 User Authentication
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])

# 5.2, 5.3, 5.4 Data Records CRUD & Retrieval
api_router.include_router(records.router, prefix="/records", tags=["Records CRUD"])

# 5.5 Dashboard & Score Analytics
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard & Analytics"])

# 5.6 Scoring Goals Configuration
api_router.include_router(goals.router, prefix="/goals", tags=["Scoring Goals"])

# Ingestion Pipelines (Text, Audio, Vision, Direct)
api_router.include_router(ingest.router, prefix="/ingest", tags=["Ingestion & AI Extraction"])

# Persistent Multi-Turn AI Chatbot
api_router.include_router(chat.router, prefix="/chat", tags=["Interactive Chatbot"])
