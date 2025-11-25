# Implementation Plan: XML Attribute Extraction

## Challenge Summary
Extract `doc-number` values from patent XML documents stored in GCS, prioritizing results by format attribute (`epo` first, then `patent-office`).

## Requirements Analysis

### Core Requirements
1. Parse XML documents containing patent application references
2. Extract all `doc-number` values from `<document-id>` elements
3. Return results in priority order: `format="epo"` first, then `format="patent-office"`
4. Handle errors uniformly and sanely
5. Use `uv` for dependency and virtual environment management

### Expected Output
Given the sample XML, the program should return:
```
['999000888', '66667777']
```

## Assumptions About Document Structure

### XML Structure Assumptions
1. **Root Element**: Document contains a `<root>` element (or similar top-level element)
2. **Application Reference**: One or more `<application-reference>` elements may exist
3. **Document ID Elements**: Each `<application-reference>` contains one or more `<document-id>` elements
4. **Format Attribute**: `<document-id>` elements have a `format` attribute with values like "epo", "patent-office", or potentially others
5. **Doc Number Element**: Each `<document-id>` contains a `<doc-number>` child element with text content
6. **Multiple Occurrences**: Multiple `<application-reference>` elements may exist in a single document
7. **Namespace Handling**: XML may or may not include namespaces (plan to handle both)
8. **Malformed XML**: Some documents may have:
   - Missing closing tags
   - Missing attributes
   - Missing `<doc-number>` elements
   - Empty `<doc-number>` elements
   - Invalid XML syntax

### Priority Order Assumptions
1. **Primary Priority**: `format="epo"` comes first
2. **Secondary Priority**: `format="patent-office"` comes second
3. **Other Formats**: Any other format values (if present) come after these two, in document order
4. **Within Same Priority**: Maintain document order for elements with the same format value
5. **Missing Format**: Elements without a `format` attribute are placed at the end

### Data Quality Assumptions
1. **Whitespace**: `<doc-number>` values may contain leading/trailing whitespace (will be stripped)
2. **Duplicates**: Same doc-number may appear multiple times (will preserve all occurrences)
3. **Empty Values**: Some `<doc-number>` elements may be empty or contain only whitespace (will be filtered out)
4. **Encoding**: XML is UTF-8 encoded (standard for XML)

## Technical Approach

### Technology Stack
- **Language**: Python 3.11+
- **XML Parsing**: `lxml` library (robust, handles malformed XML better than stdlib)
- **Web Framework**: `FastAPI` for REST API endpoints
- **ASGI Server**: `uvicorn` for production-grade async server
- **Containerization**: `Docker` with multi-stage builds
- **Package Management**: `uv` for dependency and virtual environment management
- **Testing**: `pytest` for unit tests, `httpx` for API testing

### Module Structure
```
xml_extractor/
├── __init__.py
├── extractor.py       # Main extraction logic
├── parser.py          # XML parsing utilities
└── exceptions.py      # Custom exception classes

api/
├── __init__.py
├── main.py            # FastAPI application setup
├── routes.py          # API endpoints
├── models.py          # Pydantic request/response models
└── dependencies.py    # Dependency injection

tests/
├── __init__.py
├── test_extractor.py  # Unit tests for core logic
├── test_api.py        # API integration tests
└── fixtures/          # Sample XML files (14 test cases)
    ├── README.md
    ├── 01_basic_sample/
    ├── 02_priority_ordering/
    └── ... (14 total)

main.py                # CLI entry point (backward compatibility)
Dockerfile             # Multi-stage Docker build
docker-compose.yml     # Local development setup
.dockerignore          # Docker build exclusions
README.md              # Usage instructions
pyproject.toml         # Project configuration
```

#### Core Components

**1. Parser Module (`parser.py`)**
- Responsible for loading and parsing XML
- Handle file I/O and encoding issues
- Gracefully handle malformed XML
- Return parsed XML tree or raise appropriate exceptions

**2. Extractor Module (`extractor.py`)**
- Core business logic for extracting doc-numbers
- Implement priority sorting logic
- Filter and clean extracted values
- Main public API: `extract_doc_numbers(xml_content: str) -> List[str]`

**3. Exception Module (`exceptions.py`)**
- `XMLParseError`: Raised when XML cannot be parsed
- `InvalidDocumentError`: Raised when document structure is unexpected
- `ExtractionError`: Base class for extraction-related errors

**4. API Layer (`api/`)**
- **main.py**: FastAPI application initialization, CORS, middleware
- **routes.py**: REST API endpoints for file upload and extraction
- **models.py**: Pydantic models for request validation and response serialization
- **dependencies.py**: Shared dependencies (logging, error handling)

**5. CLI Entry Point (`main.py`)** - Backward Compatibility
- CLI interface for running the extractor
- Accept file path or stdin
- Output results to stdout (one per line or JSON format)
- Handle and display errors appropriately

**6. Containerization (`Dockerfile`)**
- Multi-stage build for minimal image size
- Stage 1: Build dependencies with uv
- Stage 2: Runtime with only necessary files
- Health check endpoint
- Non-root user for security

### Error Handling Strategy

#### Error Categories
1. **File I/O Errors**
   - File not found
   - Permission denied
   - Encoding errors
   - **Action**: Log error, exit with code 1

2. **XML Parsing Errors**
   - Malformed XML syntax
   - Invalid characters
   - **Action**: Attempt recovery with lxml's lenient parser, log warnings

3. **Structure Errors**
   - Missing expected elements
   - Unexpected document structure
   - **Action**: Log warning, continue processing what's available

4. **Data Quality Issues**
   - Empty doc-numbers
   - Missing attributes
   - **Action**: Skip invalid entries, log info message

#### Error Handling Principles
- **Fail Fast**: For critical errors (file not found, completely invalid XML)
- **Graceful Degradation**: For partial data issues (missing attributes, empty values)
- **Comprehensive Logging**: All errors and warnings logged with context
- **User-Friendly Messages**: Clear error messages for end users

### Algorithm

#### Extraction Algorithm
```python
def extract_doc_numbers(xml_content: str) -> List[str]:
    1. Parse XML content into tree structure
    2. Find all <document-id> elements (handle namespaces)
    3. For each <document-id>:
       a. Extract format attribute (default to None if missing)
       b. Find <doc-number> child element
       c. Extract and clean text content
       d. Store tuple: (doc_number, format, document_order)
    4. Filter out empty/invalid doc-numbers
    5. Sort by priority:
       a. format="epo" (priority 0)
       b. format="patent-office" (priority 1)
       c. Other formats (priority 2)
       d. No format (priority 3)
       e. Within same priority, maintain document order
    6. Return list of doc-numbers (strings only)
```

#### Priority Sorting Implementation
```python
def get_priority(format_value: Optional[str]) -> int:
    priority_map = {
        'epo': 0,
        'patent-office': 1,
    }
    if format_value is None:
        return 3
    return priority_map.get(format_value, 2)
```

## Implementation Steps

### Phase 1: Project Setup ✅ (COMPLETED)
- [x] Initialize project with `uv`
- [x] Create project structure (directories and files)
- [x] Set up `pyproject.toml` with dependencies
- [x] Create basic README.md with setup instructions

### Phase 2: Core Implementation ✅ (COMPLETED)
- [x] Implement `parser.py` with XML parsing logic
- [x] Implement `exceptions.py` with custom exceptions
- [x] Implement `extractor.py` with extraction and sorting logic
- [x] Implement `main.py` CLI interface

### Phase 3: Test Fixtures ✅ (COMPLETED)
- [x] Create 14 comprehensive test fixtures covering:
  - Valid XML scenarios (5 cases)
  - Edge cases and data quality (7 cases)
  - Error/malformed XML (2 cases)
- [x] Document assumptions for each test case
- [x] Create test fixture index

### Phase 4: API Development ✅ (COMPLETED)
- [x] Create `api/` module structure
- [x] Implement FastAPI application (`api/main.py`)
- [x] Implement API routes (`api/routes.py`)
- [x] Implement Pydantic models (`api/models.py`)
- [x] Add file upload handling (multipart/form-data)
- [x] Add error handling and HTTP status codes

### Phase 5: Containerization ✅ (COMPLETED)
- [x] Create `Dockerfile` with multi-stage build
- [x] Create `docker-compose.yml` for local development
- [x] Create `.dockerignore` file
- [x] Add health check configuration

### Phase 6: Testing (IN PROGRESS)
- [ ] Test Docker build and run
- [ ] Write API integration tests (`test_api.py`)
- [ ] Test with all 14 fixture files
- [ ] Run full test suite with coverage

### Phase 7: Validation
- [ ] Verify output matches expected results
- [ ] Test error handling scenarios
- [ ] Code review and cleanup

## Testing Strategy

### Test Cases

#### Valid XML Tests
1. **Basic extraction**: Sample XML from challenge → `['999000888', '66667777']`
2. **Priority ordering**: Multiple formats in different order → correct priority
3. **Multiple application-reference elements**: All doc-numbers extracted
4. **Duplicate doc-numbers**: All preserved in order

#### Edge Cases
1. **Empty doc-number**: Filtered out
2. **Whitespace in doc-number**: Trimmed correctly
3. **Missing format attribute**: Placed at end
4. **Unknown format value**: Placed after known formats
5. **No document-id elements**: Return empty list
6. **Single document-id**: Return single-element list

#### Error Cases
1. **Malformed XML**: Graceful error or recovery
2. **Missing doc-number element**: Skip that document-id
3. **Empty XML**: Return empty list
4. **Invalid file path**: Clear error message
5. **Non-XML content**: Clear error message

### Test Data ✅ (COMPLETED)
14 comprehensive fixture files created in `tests/fixtures/`:
- See `tests/fixtures/README.md` for complete index
- Covers valid XML, edge cases, and error scenarios
- Each fixture has documented assumptions and expected outputs

## CLI Interface

### Usage
```bash
# From file
python main.py path/to/document.xml

# From stdin
cat document.xml | python main.py

# With options
python main.py --format json path/to/document.xml
python main.py --verbose path/to/document.xml
```

### Output Formats

#### Default (line-separated)
```
999000888
66667777
```

#### JSON format
```json
{
  "doc_numbers": ["999000888", "66667777"],
  "count": 2,
  "status": "success"
}
```

### Exit Codes
- `0`: Success
- `1`: File I/O error
- `2`: XML parsing error
- `3`: Invalid arguments

## Dependencies

### Production Dependencies
- `lxml>=5.0.0`: Robust XML parsing with error recovery
- `fastapi>=0.104.0`: Modern web framework for APIs
- `uvicorn[standard]>=0.24.0`: ASGI server with performance extras
- `python-multipart>=0.0.6`: File upload support
- `pydantic>=2.0.0`: Data validation (included with FastAPI)

### Development Dependencies
- `pytest>=7.0.0`: Testing framework
- `pytest-cov>=4.0.0`: Coverage reporting
- `httpx>=0.25.0`: Async HTTP client for API testing
- `black>=23.0.0`: Code formatting
- `ruff>=0.1.0`: Linting

### Container Dependencies
- `Docker`: Container runtime
- `docker-compose` (optional): Local development orchestration

## Key Decisions

- **File uploads**: API accepts file uploads (10MB limit)
- **Output format**: JSON for API, line-separated for CLI
- **Error handling**: Graceful degradation with lxml recovery parser
- **Deployment**: Docker container, runnable locally

## Success Criteria

### Core Functionality
- [ ] Correctly extracts doc-numbers from sample XML (CLI & API)
- [ ] Returns results in correct priority order
- [ ] Handles malformed XML gracefully
- [ ] Clear error messages for all error conditions

### API Requirements
- [ ] FastAPI application with proper endpoints
- [ ] File upload handling (multipart/form-data)
- [ ] Proper HTTP status codes and error responses
- [ ] OpenAPI/Swagger documentation auto-generated
- [ ] Health check endpoint for monitoring

### Containerization
- [ ] Dockerfile builds successfully
- [ ] Container runs and serves API on port 8000
- [ ] Multi-stage build for minimal image size (<200MB)
- [ ] Non-root user for security
- [ ] Health check configured

### Testing
- [ ] Comprehensive test coverage (>90%)
- [ ] All 14 fixture test cases pass
- [ ] API integration tests pass
- [ ] Docker container tests pass

### Code Quality
- [ ] Uses `uv` for dependency management
- [ ] Proper error handling and logging
- [ ] Clean, maintainable code

