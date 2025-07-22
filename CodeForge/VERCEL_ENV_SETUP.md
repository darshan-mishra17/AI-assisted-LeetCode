# 🔧 VERCEL ENVIRONMENT VARIABLE FOR FRONTEND

## 📝 Add this Environment Variable in Vercel:

**Variable Name:**
```
VITE_API_BASE_URL
```

**Variable Value:**
```
https://ai-assisted-leetcode.onrender.com
```

## 🚀 Steps to Add in Vercel:

1. Go to **Vercel Dashboard**
2. Select your **AI-assisted-LeetCode** project
3. Go to **Settings** tab
4. Click **Environment Variables** in the left sidebar
5. Click **Add** button
6. Enter:
   - **Name**: `VITE_API_BASE_URL`
   - **Value**: `https://ai-assisted-leetcode.onrender.com`
   - **Environment**: Select "Production" (and "Preview" if you want)
7. Click **Save**
8. Go to **Deployments** tab and click **Redeploy** on your latest deployment

## ✅ What This Does:

Your frontend code uses:
```typescript
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000';
```

- **Before**: Uses fallback `http://127.0.0.1:8000` (local development)
- **After**: Uses `https://ai-assisted-leetcode.onrender.com` (your deployed backend)

## 🧪 Verification:

After redeployment, check browser console on your frontend. API calls should now go to:
- ✅ `https://ai-assisted-leetcode.onrender.com/auth/login`
- ✅ `https://ai-assisted-leetcode.onrender.com/auth/signup`

Instead of the old incorrect URLs!
