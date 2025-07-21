#!/usr/bin/env python3
import sys
import os
import uvicorn
from pathlib import Path

# Get the directory where this script is located
current_dir = Path(__file__).parent.absolute()

# Add the backend directory to Python path
sys.path.insert(0, str(current_dir))
sys.path.insert(0, str(current_dir / "app"))

# Change to the backend directory
os.chdir(current_dir)

if __name__ == "__main__":
    # Start the server
    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_level="info"
    )
