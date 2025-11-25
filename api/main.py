"""
FastAPI application entry point.
"""

import time

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes import router

# Create FastAPI application
app = FastAPI(
    title="XML Doc-Number Extraction API",
    description="Extract doc-numbers from patent XML documents with priority-based ordering",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# Add CORS middleware (configure as needed for production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Track application start time for uptime calculation
app.state.start_time = time.time()

# Include API routes
app.include_router(router)


@app.get("/")
async def root():
    """
    API information endpoint.
    """
    return {
        "name": "XML Doc-Number Extraction API",
        "version": "0.1.0",
        "description": "Extract doc-numbers from patent XML documents",
        "docs_url": "/docs",
        "openapi_url": "/openapi.json",
        "endpoints": {
            "extract": "POST /extract - Upload XML file and extract doc-numbers",
            "health": "GET /health - Health check endpoint",
        },
    }


@app.get("/health")
async def health_check():
    """
    Health check endpoint for container orchestration.
    """
    uptime = time.time() - app.state.start_time
    return {
        "status": "healthy",
        "version": "0.1.0",
        "uptime_seconds": round(uptime, 2),
    }
