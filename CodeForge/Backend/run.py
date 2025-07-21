import sys
import os
import uvicorn

# Add the current directory and app directory to Python path so we can import modules
current_dir = os.path.dirname(os.path.abspath(__file__))
app_dir = os.path.join(current_dir, 'app')
sys.path.insert(0, current_dir)
sys.path.insert(0, app_dir)

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app", 
        host="127.0.0.1", 
        port=8000, 
        reload=True,
        log_level="info"
    )
