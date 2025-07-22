#!/bin/bash

echo "🔥 FINAL CORS AND AI FIX TEST 🔥"
echo "================================"

echo "1. Testing backend health..."
curl -s "https://ai-assisted-leetcode.onrender.com/health" || echo "❌ Backend is DOWN!"

echo -e "\n2. Testing CORS..."
curl -s -H "Origin: https://ai-assisted-leet-code.vercel.app" \
     -H "Access-Control-Request-Method: POST" \
     -X OPTIONS \
     "https://ai-assisted-leetcode.onrender.com/ai/hint" || echo "❌ CORS OPTIONS failed!"

echo -e "\n3. Testing AI endpoint..."
curl -s -X POST \
     -H "Content-Type: application/json" \
     -H "Origin: https://ai-assisted-leet-code.vercel.app" \
     -d '{"problem_id":"1","user_code":"// test","language":"python","hint_type":"hint"}' \
     "https://ai-assisted-leetcode.onrender.com/ai/hint" || echo "❌ AI endpoint failed!"

echo -e "\n\n🚀 If you see JSON responses above, everything is working!"
echo "If you see errors, push the backend changes and try again."
