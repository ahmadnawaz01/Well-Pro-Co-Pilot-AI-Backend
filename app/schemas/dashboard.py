from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class RecalculateScoreRequest(BaseModel):
    date: Optional[str] = Field(None, description="Target score date strictly in YYYY-MM-DD format (defaults to today)")


class RecalculateScoreResponse(BaseModel):
    success: bool = True
    message: str = "Score recalculated successfully"
    data: Optional[Dict[str, Any]] = None

