"""
Simple test script to verify CodeForge API endpoints
Run this after starting the server to test basic functionality
"""

import asyncio
import httpx
import json

BASE_URL = "http://localhost:8000"

async def test_api():
    """Test basic API functionality"""
    
    async with httpx.AsyncClient() as client:
        print("🧪 Testing CodeForge API...")
        
        # Test health endpoint
        print("\n1. Testing health endpoint...")
        response = await client.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("   ✅ Health check passed")
            print(f"   Response: {response.json()}")
        else:
            print("   ❌ Health check failed")
            return
        
        # Test user signup
        print("\n2. Testing user signup...")
        signup_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpass123",
            "full_name": "Test User"
        }
        
        response = await client.post(f"{BASE_URL}/auth/signup", json=signup_data)
        if response.status_code == 201:
            print("   ✅ User signup successful")
            user_data = response.json()
            print(f"   Created user: {user_data['username']}")
        else:
            print(f"   ❌ User signup failed: {response.text}")
            return
        
        # Test user login
        print("\n3. Testing user login...")
        login_data = {
            "username": "testuser",
            "password": "testpass123"
        }
        
        response = await client.post(f"{BASE_URL}/auth/login", json=login_data)
        if response.status_code == 200:
            print("   ✅ User login successful")
            token_data = response.json()
            access_token = token_data["access_token"]
            print("   Token received")
        else:
            print(f"   ❌ User login failed: {response.text}")
            return
        
        # Test authenticated endpoint
        print("\n4. Testing authenticated endpoint...")
        headers = {"Authorization": f"Bearer {access_token}"}
        response = await client.get(f"{BASE_URL}/auth/me", headers=headers)
        
        if response.status_code == 200:
            print("   ✅ Authentication working")
            profile = response.json()
            print(f"   User profile: {profile['username']}")
        else:
            print(f"   ❌ Authentication failed: {response.text}")
            return
        
        # Test problems endpoint
        print("\n5. Testing problems endpoint...")
        response = await client.get(f"{BASE_URL}/problems/", headers=headers)
        
        if response.status_code == 200:
            print("   ✅ Problems endpoint working")
            problems_data = response.json()
            if problems_data.get("problems"):
                print(f"   Found {len(problems_data['problems'])} problems")
                print(f"   First problem: {problems_data['problems'][0]['title']}")
            else:
                print("   No problems found (run init_db.py to add sample data)")
        else:
            print(f"   ❌ Problems endpoint failed: {response.text}")
        
        # Test leaderboard
        print("\n6. Testing leaderboard...")
        response = await client.get(f"{BASE_URL}/users/leaderboard", headers=headers)
        
        if response.status_code == 200:
            print("   ✅ Leaderboard endpoint working")
            leaderboard = response.json()
            print(f"   Leaderboard entries: {len(leaderboard.get('entries', []))}")
        else:
            print(f"   ❌ Leaderboard failed: {response.text}")
        
        # Test discussions endpoint
        print("\n7. Testing discussions...")
        response = await client.get(f"{BASE_URL}/discussions/", headers=headers)
        
        if response.status_code == 200:
            print("   ✅ Discussions endpoint working")
            discussions = response.json()
            print(f"   Found {len(discussions)} discussions")
        else:
            print(f"   ❌ Discussions failed: {response.text}")
        
        # Test AI mentor (stub)
        print("\n8. Testing AI mentor...")
        ai_request = {
            "problem_id": "507f1f77bcf86cd799439011",  # Dummy ID
            "user_code": "def solution(): pass",
            "language": "python",
            "hint_type": "explanation"
        }
        
        response = await client.post(f"{BASE_URL}/ai/hint", json=ai_request, headers=headers)
        
        if response.status_code == 200:
            print("   ✅ AI mentor endpoint working")
            hint = response.json()
            print(f"   Hint received: {hint['hint'][:50]}...")
        else:
            print(f"   ❌ AI mentor failed: {response.text}")
        
        print("\n🎉 API testing completed!")
        print("\n📝 Next steps:")
        print("   • Run init_db.py to populate with sample data")
        print("   • Integrate with Judge0 API for code execution")
        print("   • Set up AI service integration")
        print("   • Connect your frontend to these endpoints")

if __name__ == "__main__":
    print("Make sure the FastAPI server is running on http://localhost:8000")
    print("Run: cd app && python main.py")
    input("Press Enter to continue with testing...")
    asyncio.run(test_api())
