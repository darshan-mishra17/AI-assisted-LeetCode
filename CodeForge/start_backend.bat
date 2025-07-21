@echo off
echo Starting CodeForge Backend Server...
cd /d "C:\Users\HP\OneDrive\Desktop\CodeForge\Backend"

echo Setting CORS origins...
set ALLOWED_ORIGINS=http://localhost:5173,http://localhost:5174,http://127.0.0.1:5173,http://127.0.0.1:5174

echo Starting server on http://127.0.0.1:8000
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload

pause
