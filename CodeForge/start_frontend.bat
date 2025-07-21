@echo off
echo Starting CodeForge Frontend Server...
cd /d "C:\Users\HP\OneDrive\Desktop\CodeForge\Frontend"

echo Installing dependencies (if needed)...
call npm install

echo Starting React development server...
call npm run dev

pause
