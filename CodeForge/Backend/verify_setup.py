#!/usr/bin/env python3
"""
Final verification script for CodeForge problems and dashboard
"""

import asyncio
import requests
from motor.motor_asyncio import AsyncIOMotorClient

MONGODB_URL = "mongodb+srv://harshpatel:Harsh2005@cluster0.d9fud.mongodb.net/codeforge?retryWrites=true&w=majority&appName=Cluster0"

async def final_check():
    """Final verification of problems in database"""
    try:
        print("🔍 Checking CodeForge Database Status...")
        print("=" * 50)
        
        client = AsyncIOMotorClient(MONGODB_URL)
        db = client.codeforge
        problems_collection = db.problems
        
        # Count problems by difficulty
        total = await problems_collection.count_documents({})
        easy = await problems_collection.count_documents({"difficulty": "easy"})
        medium = await problems_collection.count_documents({"difficulty": "medium"})
        hard = await problems_collection.count_documents({"difficulty": "hard"})
        
        print(f"📊 DATABASE STATISTICS:")
        print(f"   Total Problems: {total}")
        print(f"   ✅ Easy: {easy}")
        print(f"   ⚡ Medium: {medium}")
        print(f"   🔥 Hard: {hard}")
        print()
        
        if total >= 20:
            print("✅ SUCCESS: Database has sufficient problems (20+)")
        elif total >= 10:
            print("⚠️  WARNING: Database has some problems but could use more")
        else:
            print("❌ ERROR: Database has too few problems")
            
        # Show sample problems
        print(f"\n📝 SAMPLE PROBLEMS:")
        sample_problems = await problems_collection.find({}).limit(5).to_list(5)
        for i, problem in enumerate(sample_problems, 1):
            print(f"   {i}. {problem['title']} ({problem['difficulty']})")
            
        client.close()
        return total
        
    except Exception as e:
        print(f"❌ Database Error: {e}")
        return 0

def test_backend_api():
    """Test if backend API is running and responding"""
    try:
        print(f"\n🚀 TESTING BACKEND API:")
        print("-" * 30)
        
        # Test problems endpoint
        response = requests.get("http://127.0.0.1:8000/problems?skip=0&limit=100", timeout=5)
        if response.status_code == 200:
            problems = response.json()
            print(f"✅ API Response: {len(problems)} problems fetched successfully")
            print(f"   Endpoint: GET /problems")
            print(f"   Status: {response.status_code}")
            return len(problems)
        else:
            print(f"❌ API Error: Status {response.status_code}")
            return 0
            
    except requests.exceptions.ConnectionError:
        print("❌ Backend API not running (Connection refused)")
        print("   💡 Start backend with: uvicorn main:app --reload --port 8000")
        return 0
    except Exception as e:
        print(f"❌ API Error: {e}")
        return 0

def main():
    print("🎯 CODEFORGE VERIFICATION REPORT")
    print("=" * 50)
    
    # Check database
    db_count = asyncio.run(final_check())
    
    # Check API
    api_count = test_backend_api()
    
    print(f"\n📋 SUMMARY:")
    print("-" * 20)
    print(f"Database Problems: {db_count}")
    print(f"API Problems: {api_count}")
    
    if db_count >= 20 and api_count >= 20:
        print("\n🎉 ALL SYSTEMS GO!")
        print("   ✅ Dashboard will now show real problem counts")
        print("   ✅ Problems page will display all available problems")
        print("   ✅ Ready for production!")
    elif db_count > 0 and api_count > 0:
        print(f"\n⚠️  PARTIALLY WORKING")
        print("   ✅ Basic functionality works")
        print("   💡 Consider adding more problems for better UX")
    else:
        print(f"\n❌ ISSUES DETECTED")
        print("   🔧 Check database connection and backend server")
        
    print(f"\n🔗 Access your application at:")
    print("   Frontend: http://localhost:5173")
    print("   Backend API: http://127.0.0.1:8000")
    print("   API Docs: http://127.0.0.1:8000/docs")

if __name__ == "__main__":
    main()
