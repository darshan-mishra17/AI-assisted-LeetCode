# 🚀 CodeForge - Launch Instructions

## Quick Start (1-Hour Launch)

### Prerequisites
- Python 3.8+ with pip
- Node.js 18+ with npm
- MongoDB Atlas account (already configured)

### Step 1: Start Backend Server

**Option A: Using PowerShell**
```powershell
cd "C:\Users\HP\OneDrive\Desktop\CodeForge"
.\start_backend.ps1
```

**Option B: Using Command Prompt**
```cmd
C:\Users\HP\OneDrive\Desktop\CodeForge\start_backend.bat
```

**Option C: Manual**
```bash
cd "C:\Users\HP\OneDrive\Desktop\CodeForge\Backend"
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

✅ **Backend should start on:** http://127.0.0.1:8000

### Step 2: Start Frontend Server

**Option A: Using PowerShell** (in new terminal)
```powershell
cd "C:\Users\HP\OneDrive\Desktop\CodeForge"
.\start_frontend.ps1
```

**Option B: Using Command Prompt** (in new terminal)
```cmd
C:\Users\HP\OneDrive\Desktop\CodeForge\start_frontend.bat
```

**Option C: Manual** (in new terminal)
```bash
cd "C:\Users\HP\OneDrive\Desktop\CodeForge\Frontend"
npm install
npm run dev
```

✅ **Frontend should start on:** http://localhost:5174

## 🎯 Test the Application

### Test Accounts:
- **Admin:** username: `admin`, password: `admin123`
- **User:** username: `johndev`, password: `password123`

### Test Flow:
1. ✅ Visit http://localhost:5174
2. ✅ Click "Sign In"
3. ✅ Login with test account
4. ✅ You should be redirected to Dashboard
5. ✅ Click "Browse Problems" to see coding problems
6. ✅ Try navigating between pages

## 🔧 Features Ready for Production

### ✅ Working Features:
- **Authentication System:** Secure JWT-based login/signup
- **Dashboard:** Real-time user stats and progress tracking
- **Problems Module:** Browse coding problems with difficulty filtering
- **User Profile:** View user statistics and achievements
- **Database Integration:** MongoDB Atlas with sample data
- **API Integration:** Full REST API with FastAPI
- **Responsive UI:** Modern glass morphism design
- **Error Handling:** Graceful error handling throughout

### 🚀 Production Ready Components:
- **Backend:** FastAPI with 9 complete modules
- **Database:** MongoDB Atlas cloud database
- **Frontend:** React + TypeScript with Vite
- **Authentication:** JWT tokens with secure storage
- **API Service:** Complete API layer with error handling
- **UI/UX:** Professional design with Tailwind CSS

## 🎨 Tech Stack

### Backend:
- **FastAPI** 0.104.1 - Modern async web framework
- **MongoDB Atlas** - Cloud database with Motor async driver
- **JWT Authentication** - Secure token-based auth
- **Groq AI** - AI mentor integration
- **Judge0 API** - Code execution service

### Frontend:
- **React 18** - Modern React with hooks
- **TypeScript** - Type-safe development
- **Vite** - Fast build tool with HMR
- **Tailwind CSS** - Utility-first styling
- **Glass Morphism** - Modern UI design

## 🌟 Key Features

### 🏠 Dashboard
- User XP and level system
- Problem-solving statistics
- Achievement badges
- Progress tracking
- Call-to-action buttons

### 📚 Problems Module
- Browse coding challenges
- Difficulty-based filtering (Easy/Medium/Hard)
- Real-time problem data from backend
- Responsive problem grid

### 🔐 Authentication
- Secure login/signup
- JWT token management
- Auto-redirect after login
- Protected routes

## 🚨 Important Notes

1. **CORS is configured** for localhost:5173, localhost:5174, and 127.0.0.1 variants
2. **Environment variables** are properly set in Backend/.env
3. **Database is pre-populated** with sample users and problems
4. **API endpoints** are fully tested and working
5. **Frontend-backend integration** is complete and functional

## 🐛 Troubleshooting

### Backend Won't Start:
```bash
# Check if MongoDB is accessible
cd Backend
python -c "from app.database import connect_to_mongo; import asyncio; asyncio.run(connect_to_mongo())"
```

### Frontend Won't Start:
```bash
cd Frontend
rm -rf node_modules package-lock.json
npm install
npm run dev
```

### CORS Errors:
- Ensure backend starts on 127.0.0.1:8000
- Ensure frontend starts on localhost:5174
- Check browser console for specific CORS errors

## 📱 Mobile Ready
The application is fully responsive and works on:
- ✅ Desktop (1920x1080)
- ✅ Tablet (768px+)
- ✅ Mobile (375px+)

## 🎉 You're Ready to Launch!

Your CodeForge application is production-ready with:
- Complete authentication system
- Real-time dashboard
- Problem browsing
- Professional UI/UX
- Full backend API
- Database integration

**Launch time: < 5 minutes** ⚡️
