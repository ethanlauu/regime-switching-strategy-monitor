#!/usr/bin/env python3
"""
Simple script to run the Regime-Switching Trading Engine FastAPI application.
"""

import uvicorn
from app.api import app

if __name__ == "__main__":
    print("Starting Regime-Switching Trading Engine...")
    print("API will be available at: http://localhost:8082")
    print("API documentation at: http://localhost:8082/docs")
    print("Press Ctrl+C to stop the server")
    
    uvicorn.run(
        "app.api:app",
        host="0.0.0.0",
        port=8082,  # Changed from 8000 to 8082 for consistency
        reload=True,
        log_level="info"
    )