"""
API route handlers for XML extraction endpoints.
"""

import time

from fastapi import APIRouter, File, UploadFile
from fastapi.responses import JSONResponse

from api.models import ErrorResponse, ExtractionResponse
from xml_extractor.exceptions import InvalidDocumentError, XMLParseError
from xml_extractor.extractor import extract_doc_numbers

router = APIRouter()

# Maximum file size: 10MB
MAX_FILE_SIZE = 10 * 1024 * 1024


@router.post(
    "/extract",
    response_model=ExtractionResponse,
    responses={
        400: {"model": ErrorResponse, "description": "XML parsing error"},
        422: {"model": ErrorResponse, "description": "Validation error"},
        500: {"model": ErrorResponse, "description": "Internal server error"},
    },
    summary="Extract doc-numbers from XML",
    description=(
        "Upload an XML file and extract all doc-numbers in priority order "
        "(epo first, then patent-office)"
    ),
)
async def extract_doc_numbers_endpoint(
    file: UploadFile = File(..., description="XML file to process")
):
    """
    Extract doc-numbers from uploaded XML file.

    The endpoint accepts an XML file upload and returns extracted doc-numbers
    in priority order:
    1. format="epo" (highest priority)
    2. format="patent-office"
    3. Other format values
    4. No format attribute (lowest priority)

    Within each priority level, document order is preserved.

    Args:
        file: Uploaded XML file (multipart/form-data)

    Returns:
        ExtractionResponse with doc-numbers, count, format breakdown, and processing time

    Raises:
        HTTPException: 400 for XML parsing errors, 422 for validation errors,
                       500 for unexpected errors
    """
    start_time = time.time()

    # Validate file type
    if file.content_type not in ["text/xml", "application/xml", None]:
        # Allow None for cases where content type isn't set
        if not file.filename.endswith(".xml"):
            return JSONResponse(
                status_code=422,
                content={
                    "error": "ValidationError",
                    "message": "Invalid file type",
                    "detail": f"Only XML files are accepted. Received: {file.content_type}",
                },
            )

    try:
        # Read file content
        content = await file.read()

        # Check file size
        if len(content) > MAX_FILE_SIZE:
            return JSONResponse(
                status_code=422,
                content={
                    "error": "ValidationError",
                    "message": "File too large",
                    "detail": f"Maximum file size is {MAX_FILE_SIZE / 1024 / 1024}MB",
                },
            )

        # Decode content
        try:
            xml_content = content.decode("utf-8")
        except UnicodeDecodeError:
            return JSONResponse(
                status_code=400,
                content={
                    "error": "EncodingError",
                    "message": "Failed to decode file",
                    "detail": "File must be UTF-8 encoded",
                },
            )

        # Extract doc-numbers
        doc_numbers = extract_doc_numbers(xml_content)

        # Calculate processing time
        processing_time = (time.time() - start_time) * 1000  # Convert to ms

        return ExtractionResponse(
            doc_numbers=doc_numbers,
            count=len(doc_numbers),
            processing_time_ms=round(processing_time, 2),
        )

    except XMLParseError as e:
        return JSONResponse(
            status_code=400,
            content={
                "error": "XMLParseError",
                "message": "Failed to parse XML document",
                "detail": str(e),
            },
        )
    except InvalidDocumentError as e:
        return JSONResponse(
            status_code=400,
            content={
                "error": "InvalidDocumentError",
                "message": "Invalid document structure",
                "detail": str(e),
            },
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "error": "InternalServerError",
                "message": "An unexpected error occurred",
                "detail": str(e),
            },
        )
