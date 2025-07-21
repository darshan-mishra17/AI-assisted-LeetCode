@echo off
echo Starting CodeForge Application...
echo.

echo Starting Frontend Development Server...
start "CodeForge Frontend" cmd /c "cd /d C:\Users\HP\OneDrive\Desktop\CodeForge\Frontend && npm run dev"

echo.
echo Frontend starting at: http://localhost:5173
echo.
echo To test the solved problems functionality:
echo 1. Go to Problems page
echo 2. Click the green "Demo: Mark First Problem as Solved" button
echo 3. Notice the circle changes to a green checkmark
echo 4. Click on any problem card to navigate to problem detail
echo.
echo Note: Backend is currently offline due to MongoDB connection issues
echo The app will work with mock data for now
echo.
pause
