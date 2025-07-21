# 🚀 Render Deployment Guide for CodeForge Backend

## Why Render?
- ✅ Free tier with 512MB RAM, 0.1 CPU
- ✅ Automatic deployments from Git
- ✅ Built-in SSL certificates
- ✅ Easy environment variable management
- ✅ No credit card required for free tier
- ✅ Better uptime than Heroku free tier

## Step-by-Step Deployment

### 1. Push Your Code to GitHub
Make sure your Backend folder is pushed to a GitHub repository.

### 2. Sign Up for Render
1. Go to [render.com](https://render.com)
2. Sign up with your GitHub account

### 3. Create New Web Service
1. Click "New" → "Web Service"
2. Connect your GitHub repository
3. Select your repository

### 4. Configure Deployment Settings
**Build & Deploy Settings:**
- **Root Directory**: `Backend` (if your backend is in a subfolder)
- **Environment**: `Python 3`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

**Plan:**
- Select "Free" plan

### 5. Environment Variables
Add these in the Render dashboard under "Environment":

```
MONGODB_URL = YOUR_MONGODB_URL_HERE
DATABASE_NAME = codeforge
SECRET_KEY = YOUR_SECURE_JWT_SECRET_KEY_HERE
ALGORITHM = HS256
ACCESS_TOKEN_EXPIRE_MINUTES = 30
ENVIRONMENT = production
ALLOWED_ORIGINS = https://ai-assisted-leet-code.vercel.app
JUDGE0_API_URL = https://judge0-ce.p.rapidapi.com
JUDGE0_API_KEY = YOUR_JUDGE0_API_KEY_HERE
GROQ_API_KEY = YOUR_GROQ_API_KEY_HERE
AI_MODEL = llama-3.1-70b-versatile
```

### 6. Deploy
1. Click "Create Web Service"
2. Render will automatically deploy your app
3. Wait for the build to complete (usually 2-3 minutes)

### 7. Get Your API URL
Your backend will be available at:
```
https://codeforge-api-xxxx.onrender.com
```
(Replace xxxx with your actual service hash)

### 8. Update Frontend
Update your frontend's Vercel environment variables:
```
VITE_API_BASE_URL = https://your-render-app-name.onrender.com
```

## Testing Your Deployment
- Health check: `https://your-app-name.onrender.com/health`
- API docs: `https://your-app-name.onrender.com/docs`

## Important Notes
- Free tier apps sleep after 15 minutes of inactivity
- First request after sleep takes ~10-30 seconds (cold start)
- Automatic deploys on every Git push to main branch
- Build logs are available in Render dashboard
- Service restarts automatically on crashes

## Troubleshooting
- Check build logs in Render dashboard
- Verify all environment variables are set correctly
- Ensure MongoDB allows connections from 0.0.0.0/0
- Check CORS settings match your frontend URL

## Alternative: One-Click Deploy
You can also use the render.yaml file for one-click deployment:
1. Add render.yaml to your repo root
2. Click "New" → "Blueprint" in Render
3. Connect your repo and deploy automatically
