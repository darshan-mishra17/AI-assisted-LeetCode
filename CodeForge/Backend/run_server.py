#!/usr/bin/env python3
"""
FastAPI Server Startup Script
"""
import sys
import os
from pathlib import Path

# Add the current directory to Python path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

# Now import and run
try:
    from app.main import app
    print("✅ Successfully imported FastAPI app")
    
    # Import uvicorn and run
    import uvicorn
    
    print("🚀 Starting CodeForge Backend Server...")
    print("📍 Backend running on: http://localhost:8000")
    print("📚 API Docs available at: http://localhost:8000/docs")
    print("🤖 AI Mentor ready to help!")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8001,  # Use different port
        reload=False  # Disable reload to avoid subprocess issues
    )
    
except Exception as e:
    print(f"❌ Failed to start server: {e}")
    import traceback
    traceback.print_exc()
