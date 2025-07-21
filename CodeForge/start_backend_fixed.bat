@echo off
echo Starting CodeForge Backend Server...
cd /d "C:\Users\HP\OneDrive\Desktop\CodeForge\Backend"
python -m uvicorn main:app --reload --port 8000
