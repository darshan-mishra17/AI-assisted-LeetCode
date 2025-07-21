#!/bin/bash
# Deploy script for Render

echo "🚀 Preparing for Render deployment..."

# Add all changes
git add .

# Commit changes
git commit -m "Configure for Render deployment"

# Push to GitHub (make sure you have a remote set up)
git push origin main

echo "✅ Code pushed to GitHub!"
echo "🌐 Now go to render.com and create a new Web Service"
echo "📁 Root Directory: Backend"
echo "🐍 Environment: Python 3"
echo "🔨 Build Command: pip install -r requirements.txt"
echo "▶️  Start Command: uvicorn app.main:app --host 0.0.0.0 --port \$PORT"
