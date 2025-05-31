#!/usr/bin/env python3
"""
Spam Detection API
Main FastAPI application entry point
"""

import time
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from core.config import get_settings
from core.logging import setup_logging, get_logger
from core.ml_loader import initialize_models
from api.endpoints import analysis, health, admin
from api.models import ErrorResponse


# Setup logging first
setup_logging()
logger = get_logger()

# Get settings
settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    logger.info("🚀 Starting Spam Detection API...")
    
    # Initialize ML models
    logger.info("Loading ML models...")
    models_loaded = initialize_models()
    if models_loaded:
        logger.success("✅ ML models loaded successfully")
    else:
        logger.error("❌ Failed to load ML models")
    
    logger.info(f"🌐 API will be available at http://{settings.api_host}:{settings.api_port}")
    logger.info("📚 API documentation at /docs")
    
    yield
    
    # Shutdown
    logger.info("🛑 Shutting down Spam Detection API...")


# Create FastAPI application
app = FastAPI(
    title=settings.api_title,
    version=settings.api_version,
    description="""
    ## Spam Detection API
    
    A comprehensive spam detection system that combines text classification with phone number validation 
    to make intelligent decisions about message legitimacy.
    
    ### Features:
    - **Text Classification**: ML-powered spam/ham detection using MultinomialNB
    - **Phone Validation**: Risk assessment using phone number database
    - **Decision Matrix**: 4-tier decision system (CLEAN/CONTENT_WARNING/SENDER_WARNING/BLOCKED)
    - **Real-time Analysis**: Sub-20ms response times
    - **Health Monitoring**: System status and statistics
    - **Admin Tools**: Configuration management and training data
    
    ### Decision Outcomes:
    - **CLEAN**: Safe message from trusted source
    - **CONTENT_WARNING**: Potentially suspicious content, review recommended
    - **SENDER_WARNING**: Suspicious sender, content may be legitimate
    - **BLOCKED**: High confidence spam, recommend blocking
    """,
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
    debug=settings.debug
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request timing middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """Add processing time to response headers"""
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(f"{process_time:.3f}")
    return response


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Handle unexpected errors gracefully"""
    logger.error(f"Unhandled exception in {request.method} {request.url}: {str(exc)}")
    
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            error="InternalServerError",
            message="An unexpected error occurred while processing your request",
            details={"path": str(request.url), "method": request.method}
        ).dict()
    )


# Include routers
app.include_router(analysis.router, prefix="/api/v1", tags=["Message Analysis"])
app.include_router(health.router, prefix="/api/v1", tags=["Health & Monitoring"])
app.include_router(admin.router, prefix="/api/v1/admin", tags=["Administration"])


# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    """API root endpoint with basic information"""
    return {
        "message": "Spam Detection API",
        "version": settings.api_version,
        "status": "operational",
        "docs": "/docs",
        "health": "/api/v1/health"
    }


if __name__ == "__main__":
    import uvicorn
    
    logger.info(f"Starting server on {settings.api_host}:{settings.api_port}")
    uvicorn.run(
        "main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.debug,
        log_level="info"
    ) 