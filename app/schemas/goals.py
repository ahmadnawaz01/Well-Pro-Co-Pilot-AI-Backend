from typing import Any, Dict, Optional
from pydantic import BaseModel, Field


class SetupGoalsRequest(BaseModel):
    goals: Dict[str, Any] = Field(
        ...,
        description="Dictionary of wellbeing goals (e.g. {'steps': '12k', 'financial_budget': '$3,500', 'savings_rate': '25%', 'water': '3L', 'exercise_minutes': 45})"
    )
    recalculate: bool = Field(
        True,
        description="Whether to immediately recalculate current scores with the updated targets"
    )


class GoalsResponse(BaseModel):
    success: bool = True
    message: str
    data: Optional[Dict[str, Any]] = None

