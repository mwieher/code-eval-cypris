# Architecture Overview

## System Design

This is a microservice-based XML extraction system with three deployment modes: Python library, CLI tool, and REST API.

## Components

### Core Layer (`xml_extractor/`)

**Purpose**: Business logic for extracting and prioritizing doc-numbers from XML.

- **`parser.py`**: XML parsing with lxml recovery mode for malformed documents
- **`extractor.py`**: Priority-based extraction algorithm
- **`exceptions.py`**: Custom exception hierarchy

**Key Algorithm**:
```
1. Parse XML with error recovery
2. Find all <document-id> elements via XPath
3. Extract format attribute and <doc-number> text
4. Assign priority: epo=0, patent-office=1, other=2, none=3
5. Sort by (priority, document_order)
6. Return doc-numbers as list
```

### API Layer (`api/`)

**Purpose**: REST API wrapper for HTTP-based access.

- **`main.py`**: FastAPI application initialization, CORS, health tracking
- **`routes.py`**: Endpoint handlers with file upload validation
- **`models.py`**: Pydantic request/response schemas
- **`dependencies.py`**: Shared dependencies (logging)

**Endpoints**:
- `POST /extract`: Upload XML file, returns JSON with doc-numbers
- `GET /health`: Container health check
- `GET /docs`: Auto-generated OpenAPI documentation

### CLI (`main.py`)

**Purpose**: Command-line interface for batch processing.

- Reads from file or stdin
- Outputs one doc-number per line
- Exit codes: 0=success, 1=file error, 2=extraction error, 3=unexpected

### Containerization

**Dockerfile**: Multi-stage build
- Stage 1 (builder): Install dependencies with uv
- Stage 2 (runtime): Minimal image with non-root user (UID 1000)
- Health check: Python urllib (no curl dependency)

**docker-compose.yml**: Local development
- Volume mounts for hot-reload
- Port 8000 exposed
- Development mode with `--reload`

## Data Flow

### Library Usage
```
User Code → extract_doc_numbers() → Parser → Extractor → List[str]
```

### CLI Usage
```
File/Stdin → main.py → extract_doc_numbers() → stdout (line-separated)
```

### API Usage
```
HTTP POST → FastAPI → File Validation → extract_doc_numbers() → JSON Response
```

## Error Handling

**Strategy**: Graceful degradation with clear error messages

- **XML Parse Errors**: lxml recovery parser attempts to salvage partial data
- **Missing Elements**: Skip and continue processing
- **Empty Values**: Filter out after extraction
- **File Errors**: Return appropriate HTTP status codes (400, 422, 500)

## Technology Choices

- **lxml**: Robust XML parsing with recovery mode for malformed documents
- **FastAPI**: Modern async framework with auto-generated OpenAPI docs
- **uvicorn**: High-performance ASGI server
- **uv**: Fast dependency management (10-100x faster than pip)
- **Docker**: Containerization for consistent deployment
- **pytest**: Testing framework with coverage support

## Scalability Considerations

- **Stateless**: No session state, horizontally scalable
- **Async**: FastAPI supports async for I/O-bound operations
- **File Size Limit**: 10MB default (configurable)
- **Memory**: Tree-based parsing (suitable for documents <10MB)
- **Performance**: <1ms processing time for typical patent documents

## Security

- **Non-root container**: Runs as UID 1000
- **File validation**: Type and size checks before processing
- **Input sanitization**: lxml handles XML injection risks
- **No authentication**: Designed for internal use (add API keys if needed)

## Testing

- **Unit tests**: Core extraction logic (`tests/test_extractor.py`)
- **Fixtures**: 14 comprehensive test cases covering edge cases
- **API tests**: File upload, error handling, validation
- **Coverage**: Pytest with coverage reporting

## Deployment Options

1. **Local Development**: `uv` + virtual environment
2. **Docker Compose**: Single-command local deployment
3. **Container Orchestration**: K8s, Cloud Run, ECS (production-ready)
4. **Serverless**: Can be adapted for AWS Lambda, Cloud Functions

