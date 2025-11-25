"""
Pydantic models for request validation and response serialization.
"""

from pydantic import BaseModel, Field


class ExtractionResponse(BaseModel):
    """
    Response model for successful doc-number extraction.
    """

    doc_numbers: list[str] = Field(
        ...,
        description="List of extracted doc-numbers in priority order",
        example=["999000888", "66667777"],
    )
    count: int = Field(..., description="Total number of doc-numbers extracted", example=2)
    processing_time_ms: float = Field(
        ..., description="Processing time in milliseconds", example=12.5
    )


class ErrorResponse(BaseModel):
    """
    Response model for errors.
    """

    error: str = Field(..., description="Error type", example="XMLParseError")
    message: str = Field(
        ...,
        description="Human-readable error message",
        example="Failed to parse XML document",
    )
    detail: str = Field(
        default="",
        description="Technical details for debugging",
        example="Line 5: Opening and ending tag mismatch",
    )
