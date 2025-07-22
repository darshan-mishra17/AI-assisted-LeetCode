# 🚀 QUICK DEPLOYMENT SETUP - CodeForge

## 📋 Your Configuration Summary

**Frontend**: ✅ `https://ai-assisted-leet-code.vercel.app`
**Backend**: 🔄 Deploy to Render with these settings

## 🔑 Copy-Paste Environment Variables for Render:

```
MONGODB_URL=mongodb+srv://hardikpandu123654:QwertyuioP1234@cluster0.cisbozq.mongodb.net/codeforge
DATABASE_NAME=codeforge
SECRET_KEY=your-super-secret-key-change-this-in-production-render-2025
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
ENVIRONMENT=production
PORT=8000
GROQ_API_KEY=your-groq-api-key-here
AI_MODEL=llama-3.1-8b-instant
JUDGE0_API_URL=https://judge0-ce.p.rapidapi.com
JUDGE0_API_KEY=your-judge0-api-key-here
AI_MENTOR_MODEL=llama-3.1-8b-instant
AI_MENTOR_TEMPERATURE=0.1
AI_MENTOR_MAX_TOKENS=4096
ENABLE_ADVANCED_AI=true
ENABLE_CONVERSATION_HISTORY=true
ALLOWED_ORIGINS=https://ai-assisted-leet-code.vercel.app,https://localhost:5173
```

## 🏃‍♂️ Deployment Steps:

1. **Deploy Backend to Render**:
   - Service Type: Web Service
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - Root Directory: `Backend`
   - Add all environment variables above

2. **Update Frontend Environment**:
   - After backend is deployed, get the Render URL (e.g., `https://your-backend.onrender.com`)
   - In Vercel Dashboard > Settings > Environment Variables
   - Add: `VITE_API_BASE_URL=https://your-backend.onrender.com`
   - Redeploy frontend

## 🧪 Test After Deployment:

1. Visit your backend: `https://your-backend.onrender.com/docs`
2. Test CORS: `https://your-backend.onrender.com/cors-test`
3. Test AI Mentor: `https://your-backend.onrender.com/ai/status`
4. Test frontend: `https://ai-assisted-leet-code.vercel.app`

## ✅ Ready to Deploy!

Your CORS is already configured for your Vercel frontend URL. Just deploy the backend and update the frontend API URL! 🎉
