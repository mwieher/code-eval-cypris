# Multi-stage Docker build for XML Extractor API
# Stage 1: Builder - Install dependencies
FROM python:3.11-slim AS builder

WORKDIR /app

# Install uv for fast dependency management
RUN pip install --no-cache-dir uv

# Copy dependency files
COPY pyproject.toml README.md ./

# Copy source code (needed for package installation)
COPY xml_extractor/ ./xml_extractor/
COPY api/ ./api/

# Create virtual environment and install production dependencies only
RUN uv venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN uv pip install --no-cache .

# Stage 2: Runtime - Minimal production image
FROM python:3.11-slim

WORKDIR /app

# Copy virtual environment from builder stage
COPY --from=builder /opt/venv /opt/venv

# Copy application code
COPY xml_extractor/ ./xml_extractor/
COPY api/ ./api/

# Use virtual environment
ENV PATH="/opt/venv/bin:$PATH"

# Environment variables for configuration
ENV MAX_FILE_SIZE=10485760
ENV LOG_LEVEL=INFO

# Create non-root user for security
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 8000

# Health check using Python's built-in urllib (no curl dependency needed)
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

# Run application
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]

