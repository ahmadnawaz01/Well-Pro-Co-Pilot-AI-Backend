from fastapi import APIRouter, Depends, status, Query
from pydantic import BaseModel, Field
from typing import List, Dict, Any

from app.api.deps import verify_frappe_token
from app.schemas.auth import UserSessionData
from app.services.chatbot_service import (
    execute_chat_message,
    fetch_user_chat_history,
    clear_user_chat_history,
)

router = APIRouter()


class ChatMessageRequest(BaseModel):
    message: str = Field(..., description="User prompt or message")
    session_id: str = Field(default="default", description="Session thread ID")


class ChatMessageResponse(BaseModel):
    status: str
    user_email: str
    session_id: str
    response: str


@router.post("/message", response_model=ChatMessageResponse, status_code=status.HTTP_200_OK)
async def send_chat_message(
    payload: ChatMessageRequest,
    session: UserSessionData = Depends(verify_frappe_token)
):
    """
    1. Interactive multi-turn chat endpoint with tool calls to Frappe.
    2. Context is strictly isolated per thread (user_email:session_id).
    """
    agent_response = await execute_chat_message(
        user_email=session.user_email,
        raw_token=session.raw_token,
        message=payload.message,
        session_id=payload.session_id
    )

    return ChatMessageResponse(
        status="success",
        user_email=session.user_email,
        session_id=payload.session_id,
        response=agent_response
    )


@router.get("/history", status_code=status.HTTP_200_OK)
async def get_chat_history(
    session_id: str = Query(default="default"),
    session: UserSessionData = Depends(verify_frappe_token)
):
    """
    Retrieves full chat message history from MongoDB to rehydrate frontend UI on page load or refresh.
    """
    history = await fetch_user_chat_history(
        user_email=session.user_email,
        session_id=session_id
    )

    return {
        "status": "success",
        "user_email": session.user_email,
        "session_id": session_id,
        "count": len(history),
        "messages": history
    }


@router.delete("/clear", status_code=status.HTTP_200_OK)
async def clear_chat(
    session_id: str = Query(default="default"),
    session: UserSessionData = Depends(verify_frappe_token)
):
    """
    Clears the chat history in MongoDB for the given user session.
    """
    await clear_user_chat_history(
        user_email=session.user_email,
        session_id=session_id
    )

    return {
        "status": "success",
        "message": f"Chat history cleared for session '{session_id}'.",
        "user_email": session.user_email
    }