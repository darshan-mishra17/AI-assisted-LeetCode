# 🚀 RENDER DEPLOYMENT GUIDE - CodeForge Backend

## 📋 Pre-Deployment Checklist

### ✅ Required Files in Your Repository:
- [ ] `requirements.txt` (Python dependencies)
- [ ] `Procfile` or startup command configuration
- [ ] `app/main.py` (FastAPI application entry point)

### ✅ Environment Variables Setup on Render:

Copy and paste these environment variables in your Render dashboard:

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
```

**⚠️ IMPORTANT: CORS is already configured for your frontend:**
```
ALLOWED_ORIGINS=https://ai-assisted-leet-code.vercel.app,https://localhost:5173
```

After your **backend** is deployed, update your frontend environment:

## 🔧 Render Service Configuration

### Build Command:
```bash
pip install -r requirements.txt
```

### Start Command:
```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

### Root Directory:
```
Backend
```

### Environment:
- **Python Version**: 3.9+ (recommended: 3.11)
- **Region**: Choose closest to your users
- **Service Type**: Web Service

## 🌐 CORS Configuration

After your backend is deployed:

1. **Get your backend URL** from Render (e.g., `https://codeforge-backend.onrender.com`)
2. **CORS is already configured** for `https://ai-assisted-leet-code.vercel.app`
3. **Update your frontend** environment variable in Vercel:
   - Go to Vercel Dashboard > Your Project > Settings > Environment Variables
   - Set: `VITE_API_BASE_URL=https://your-backend-name.onrender.com`

## 🧪 Testing After Deployment

### Health Check Endpoints:
- `https://your-backend.onrender.com/` - Basic API info
- `https://your-backend.onrender.com/health` - Health status  
- `https://your-backend.onrender.com/docs` - API documentation
- `https://your-backend.onrender.com/cors-test` - CORS verification

### AI Mentor Test:
- `https://your-backend.onrender.com/ai/status` - AI mentor status

## 🚨 Common Issues & Solutions

### Issue: "App failed to start"
- **Solution**: Check logs for missing dependencies in `requirements.txt`

### Issue: "Port already in use"  
- **Solution**: Ensure start command uses `--port $PORT`

### Issue: "CORS errors"
- **Solution**: Update `ALLOWED_ORIGINS` with your frontend URL

### Issue: "Database connection failed"
- **Solution**: Verify `MONGODB_URL` in environment variables

### Issue: "AI Mentor not working"
- **Solution**: Check `GROQ_API_KEY` is correctly set

## 📝 Notes

- **Free Tier Limitations**: Service may sleep after 15 minutes of inactivity
- **Cold Starts**: First request after sleep may take 30-60 seconds
- **Logs**: Check Render logs for debugging deployment issues
- **Environment**: Always set `ENVIRONMENT=production` for live deployment

## 🔐 Security Recommendations

1. **Change SECRET_KEY** to a strong, unique value for production
2. **Restrict CORS** to only your frontend domains
3. **Enable HTTPS** (Render does this automatically)
4. **Monitor API usage** to prevent abuse
5. **Rotate API keys** periodically

---
**🎉 Ready to Deploy!** 
Push your code to GitHub and connect it to Render with these configurations.
