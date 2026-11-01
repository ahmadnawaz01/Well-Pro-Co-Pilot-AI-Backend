from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel, Field


class UpdateRecordRequest(BaseModel):
    doctype: str = Field(..., description="Target Frappe DocType name")
    name: str = Field(..., description="Target document ID/name")
    update_data: Dict[str, Any] = Field(..., description="Key-value dictionary of updated fields")


class DeleteRecordRequest(BaseModel):
    doctype: str = Field(..., description="Target Frappe DocType name")
    name: str = Field(..., description="Target document ID/name to delete")


class GetUserRecordsQuery(BaseModel):
    doctype: str = Field(..., description="Frappe DocType name (e.g. 'Financial Transaction')")
    limit: int = Field(50, ge=1, le=200, description="Max records to return")
    offset: int = Field(0, ge=0, description="Offset for pagination")
    order_by: Optional[str] = Field(None, description="Sorting string, e.g. 'transaction_date desc'")
    from_date: Optional[str] = Field(None, description="Filter records from date (YYYY-MM-DD)")
    to_date: Optional[str] = Field(None, description="Filter records to date (YYYY-MM-DD)")


class GenericSuccessResponse(BaseModel):
    success: bool = True
    message: str
    data: Optional[Any] = None

