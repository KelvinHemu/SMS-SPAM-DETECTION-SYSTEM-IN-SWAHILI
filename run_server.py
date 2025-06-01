#!/usr/bin/env python3
"""
Simple server launcher with increased limits
"""

import uvicorn
from core.config import get_settings

if __name__ == "__main__":
    settings = get_settings()
    
    print(f"🚀 Starting Spam Detection API server...")
    print(f"📍 Host: {settings.api_host}")
    print(f"🔌 Port: {settings.api_port}")
    print(f"📚 Docs: http://{settings.api_host}:{settings.api_port}/docs")
    
    # Start server with increased limits to prevent 431 errors
    uvicorn.run(
        "main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=False,  # Disable reload to reduce overhead
        log_level="info",
        # Increase limits to prevent 431 Request Header Fields Too Large
        limit_max_requests=1000,
        limit_concurrency=100,
        timeout_keep_alive=30,
        # Additional uvicorn settings
        access_log=True,
        workers=1  # Single worker for development
    ) 