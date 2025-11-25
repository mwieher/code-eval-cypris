# XML Doc-Number Extractor

Extract `doc-number` values from patent XML documents with priority-based ordering.

## Requirements

- Python 3.11+
- [uv](https://github.com/astral-sh/uv) package manager
- Docker (for containerized deployment)

## Local Development Setup

```bash
# Create and activate virtual environment
uv venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # macOS/Linux

# Install dependencies
uv pip install -e ".[dev]"

# Run CLI
python main.py path/to/file.xml

# Use as a library
python
>>> from xml_extractor import extract_doc_numbers
>>> xml_content = open('sample.xml').read()
>>> doc_numbers = extract_doc_numbers(xml_content)
>>> print(doc_numbers)
['999000888', '66667777']
```

## Testing

### Run Unit Tests
```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run with coverage
pytest --cov=xml_extractor --cov=api
```

### Linting and Formatting
```bash
# Format code with black
black .

# Check formatting without making changes
black --check .

# Lint with ruff
ruff check .

# Auto-fix linting issues
ruff check --fix .

# Run both checks
black --check . && ruff check .
```

### Test with Fixtures (CLI)
```bash
# Test basic sample
python main.py tests/fixtures/01_basic_sample/input.xml

# Test priority ordering
python main.py tests/fixtures/02_priority_ordering/input.xml

# Test large document
python main.py tests/fixtures/13_large_document/input.xml
```

### Test with Fixtures (API)
```bash
# Start the container
docker-compose up -d

# Test with fixture files (cure.exe for Windows PowerShell, curl on macOS/Linux)
curl.exe -X POST http://localhost:8000/extract -F "file=@tests/fixtures/01_basic_sample/input.xml"
curl.exe -X POST http://localhost:8000/extract -F "file=@tests/fixtures/02_priority_ordering/input.xml"


# All 14 fixtures are available in tests/fixtures/
# See tests/fixtures/README.md for complete list
```

## Docker Usage

```bash
# Build and run with docker-compose
docker-compose up

# Or build and run manually
docker build -t xml-extractor .
docker run -p 8000:8000 xml-extractor

# Test the API (use curl.exe on Windows PowerShell)
curl.exe http://localhost:8000/health
curl.exe -X POST http://localhost:8000/extract -F "file=@sample.xml"

# Or use PowerShell native commands
Invoke-RestMethod -Uri "http://localhost:8000/health"
Invoke-RestMethod -Uri "http://localhost:8000/extract" -Method Post -Form @{file = Get-Item "sample.xml"}

# View API docs
open http://localhost:8000/docs
```

## API Endpoints

- `POST /extract` - Upload XML file, returns extracted doc-numbers
- `GET /health` - Health check
- `GET /docs` - Interactive API documentation

## Priority Order

1. `format="epo"` (highest priority)
2. `format="patent-office"`
3. Other format values
4. No format attribute (lowest priority)
