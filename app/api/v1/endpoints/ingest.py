from fastapi import File, UploadFile, Depends, status, APIRouter, Body
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional, Union

from app.api.deps import verify_frappe_token
from app.core.database import get_database
from app.schemas.auth import UserSessionData
from app.services.whisper_service import transcribe_and_translate_audio
from app.services.graph_service import run_ingestion_pipeline
from app.services.frappe_dispatch import dispatch_records_to_frappe
from app.services.frappe_client import FrappeClient
from app.services.mongo_service import log_ingestion_event
from app.services.openrouter_service import extract_text_from_image

router = APIRouter()


class IngestTextRequest(BaseModel):
    raw_text: str = Field(..., min_length=2, description="User raw text or transcript to process")


class IngestTextResponse(BaseModel):
    status: str
    user_email: str
    extracted_count: int
    extracted_records: List[Dict[str, Any]]
    frappe_dispatch_results: List[Dict[str, Any]]
    recalculated_scores: Optional[Dict[str, Any]] = None
    mongo_log_id: str
    validation_error: Optional[str] = None


class IngestAudioResponse(BaseModel):
    status: str
    user_email: str
    transcribed_english_text: str
    is_relevant: bool
    relevance_reason: Optional[str]
    extracted_count: int
    extracted_records: List[Dict[str, Any]]
    frappe_dispatch_results: List[Dict[str, Any]]
    recalculated_scores: Optional[Dict[str, Any]] = None
    mongo_log_id: str


class IngestImageResponse(BaseModel):
    status: str
    user_email: str
    extracted_ocr_text: str
    is_relevant: bool
    relevance_reason: Optional[str]
    extracted_count: int
    extracted_records: List[Dict[str, Any]]
    frappe_dispatch_results: List[Dict[str, Any]]
    recalculated_scores: Optional[Dict[str, Any]] = None
    mongo_log_id: str


@router.post("/process-text", response_model=IngestTextResponse, status_code=status.HTTP_200_OK)
async def process_text_ingestion(
    payload: IngestTextRequest,
    session: UserSessionData = Depends(verify_frappe_token)
):
    """
    Main text ingestion endpoint:
    1. Verifies user token with Frappe RPC.
    2. Runs Gemini structured extraction pipeline.
    3. Dispatches extracted items to Frappe v2.0.0 store_ai_record.
    4. Archives full logs and response payload to MongoDB Atlas.
    5. Returns extracted data and newly calculated wellbeing scores.
    """
    # 1. Run extraction pipeline
    graph_result = await run_ingestion_pipeline(raw_text=payload.raw_text)
    extracted_records = graph_result.get("records", [])
    validation_error = graph_result.get("validation_error")

    # 2. Dispatch to Frappe
    frappe_dispatch_results = []
    recalculated_scores = None
    if extracted_records:
        frappe_dispatch_results = await dispatch_records_to_frappe(
            records=extracted_records,
            raw_token=session.raw_token
        )
        if frappe_dispatch_results and frappe_dispatch_results[0].get("status") == "success":
            recalculated_scores = frappe_dispatch_results[0].get("recalculated_scores")

    # 3. Log event to MongoDB Atlas
    db = get_database()
    mongo_id = await log_ingestion_event(
        db=db,
        session=session,
        raw_text=payload.raw_text,
        extracted_records=extracted_records,
        frappe_dispatch_results=frappe_dispatch_results,
        execution_error=validation_error
    )

    return IngestTextResponse(
        status="success" if not validation_error else "partial_success",
        user_email=session.user_email,
        extracted_count=len(extracted_records),
        extracted_records=extracted_records,
        frappe_dispatch_results=frappe_dispatch_results,
        recalculated_scores=recalculated_scores,
        mongo_log_id=mongo_id,
        validation_error=validation_error
    )


@router.post("/process-audio", response_model=IngestAudioResponse, status_code=status.HTTP_200_OK)
async def process_audio_ingestion(
    file: UploadFile = File(...),
    session: UserSessionData = Depends(verify_frappe_token)
):
    """
    Multilingual audio ingestion endpoint:
    1. Authenticates Frappe token from header.
    2. Transcribes & translates audio into English via Groq Whisper large-v3.
    3. Runs Gemini extraction pipeline to extract structured health, finance, and social metrics.
    4. Dispatches records directly to Frappe store_ai_record.
    5. Archives complete event log in MongoDB Atlas.
    """
    # 1. Groq Audio Transcription & Translation to English
    english_text = await transcribe_and_translate_audio(file)

    # 2. Execute Extraction Pipeline
    graph_result = await run_ingestion_pipeline(raw_text=english_text)

    is_relevant = graph_result.get("is_relevant", False)
    relevance_reason = graph_result.get("relevance_reason")
    extracted_records = graph_result.get("records", [])
    validation_error = graph_result.get("validation_error")

    # 3. Dispatch to Frappe if relevant
    frappe_dispatch_results = []
    recalculated_scores = None
    if is_relevant and extracted_records:
        frappe_dispatch_results = await dispatch_records_to_frappe(
            records=extracted_records,
            raw_token=session.raw_token
        )
        if frappe_dispatch_results and frappe_dispatch_results[0].get("status") == "success":
            recalculated_scores = frappe_dispatch_results[0].get("recalculated_scores")

    # 4. Log to MongoDB Atlas
    db = get_database()
    mongo_id = await log_ingestion_event(
        db=db,
        session=session,
        raw_text=f"[AUDIO TRANSCRIPT]: {english_text}",
        extracted_records=extracted_records,
        frappe_dispatch_results=frappe_dispatch_results,
        execution_error=validation_error if is_relevant else f"Aborted: {relevance_reason}"
    )

    return IngestAudioResponse(
        status="success" if is_relevant else "ignored_off_topic",
        user_email=session.user_email,
        transcribed_english_text=english_text,
        is_relevant=is_relevant,
        relevance_reason=relevance_reason,
        extracted_count=len(extracted_records),
        extracted_records=extracted_records,
        frappe_dispatch_results=frappe_dispatch_results,
        recalculated_scores=recalculated_scores,
        mongo_log_id=mongo_id
    )


@router.post("/process-image", response_model=IngestImageResponse, status_code=status.HTTP_200_OK)
async def process_image_ingestion(
    file: UploadFile = File(...),
    session: UserSessionData = Depends(verify_frappe_token)
):
    """
    OCR document/receipt ingestion endpoint:
    1. Authenticates Frappe token from header.
    2. Extracts raw text from uploaded document image using OpenRouter Vision API.
    3. Runs Gemini structured extraction to produce validated records.
    4. Dispatches records directly to Frappe store_ai_record.
    5. Records full audit event in MongoDB Atlas.
    """
    # 1. OCR Extraction via OpenRouter Vision
    ocr_text = await extract_text_from_image(file)

    # 2. Structured Extraction
    graph_result = await run_ingestion_pipeline(raw_text=ocr_text)

    is_relevant = graph_result.get("is_relevant", False)
    relevance_reason = graph_result.get("relevance_reason")
    extracted_records = graph_result.get("records", [])
    validation_error = graph_result.get("validation_error")

    # 3. Dispatch to Frappe
    frappe_dispatch_results = []
    recalculated_scores = None
    if is_relevant and extracted_records:
        frappe_dispatch_results = await dispatch_records_to_frappe(
            records=extracted_records,
            raw_token=session.raw_token
        )
        if frappe_dispatch_results and frappe_dispatch_results[0].get("status") == "success":
            recalculated_scores = frappe_dispatch_results[0].get("recalculated_scores")

    # 4. Save Audit Record in MongoDB
    db = get_database()
    mongo_id = await log_ingestion_event(
        db=db,
        session=session,
        raw_text=f"[IMAGE OCR TRANSCRIPT]: {ocr_text}",
        extracted_records=extracted_records,
        frappe_dispatch_results=frappe_dispatch_results,
        execution_error=validation_error if is_relevant else f"Aborted: {relevance_reason}"
    )

    return IngestImageResponse(
        status="success" if is_relevant else "ignored_off_topic",
        user_email=session.user_email,
        extracted_ocr_text=ocr_text,
        is_relevant=is_relevant,
        relevance_reason=relevance_reason,
        extracted_count=len(extracted_records),
        extracted_records=extracted_records,
        frappe_dispatch_results=frappe_dispatch_results,
        recalculated_scores=recalculated_scores,
        mongo_log_id=mongo_id
    )


@router.post(
    "/insert-record",
    status_code=status.HTTP_200_OK,
    summary="Direct Ingestion Proxy (insert_record)",
    description="Ingests structured records directly into Frappe v2.0.0 insert_record (supports multi-doctype, single, or batch)."
)
async def direct_insert_record(
    payload: Union[Dict[str, Any], List[Dict[str, Any]]] = Body(...),
    session: UserSessionData = Depends(verify_frappe_token),
):
    return await FrappeClient.insert_record(payload=payload, token=session.raw_token)


@router.post(
    "/store-ai-record",
    status_code=status.HTTP_200_OK,
    summary="Direct AI Record Storage (store_ai_record)",
    description="Stores structured domain records directly into Frappe v2.0.0 store_ai_record with AI Extraction provenance."
)
async def direct_store_ai_record(
    payload: Dict[str, Any] = Body(...),
    session: UserSessionData = Depends(verify_frappe_token),
):
    return await FrappeClient.store_ai_record(payload=payload, token=session.raw_token)
