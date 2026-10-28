from typing import TypedDict, List, Dict, Any, Optional
from langgraph.graph import StateGraph, END

from app.services.gemini_service import extract_structured_records_single_pass
from app.schemas.extraction import ExtractionResponse


class IngestionState(TypedDict):
    raw_text: str
    is_relevant: bool
    relevance_reason: Optional[str]
    extracted_records: List[Dict[str, Any]]
    validation_error: Optional[str]


async def single_pass_extract_node(state: IngestionState) -> Dict[str, Any]:
    """Single-pass node that evaluates relevance and extracts records in one LLM call."""
    response: ExtractionResponse = await extract_structured_records_single_pass(state["raw_text"])
    
    records_dict = [rec.model_dump() for rec in response.records] if response.records else []
    
    return {
        "is_relevant": response.is_relevant,
        "relevance_reason": response.relevance_reason,
        "extracted_records": records_dict,
        "validation_error": None
    }


def build_ingestion_graph():
    builder = StateGraph(IngestionState)
    builder.add_node("extract_and_validate", single_pass_extract_node)
    builder.set_entry_point("extract_and_validate")
    builder.add_edge("extract_and_validate", END)
    return builder.compile()


ingestion_graph = build_ingestion_graph()


async def run_ingestion_pipeline(raw_text: str) -> Dict[str, Any]:
    initial_state: IngestionState = {
        "raw_text": raw_text,
        "is_relevant": False,
        "relevance_reason": None,
        "extracted_records": [],
        "validation_error": None
    }

    final_state = await ingestion_graph.ainvoke(initial_state)

    return {
        "is_relevant": final_state.get("is_relevant", False),
        "relevance_reason": final_state.get("relevance_reason"),
        "records": final_state.get("extracted_records", []),
        "validation_error": final_state.get("validation_error"),
        "retry_count": 0
    }