#!/usr/bin/env python3
"""
Test MongoDB connection with different approaches
"""

import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import pymongo

# Different connection strings to try
MONGODB_URLS = [
    "mongodb+srv://harshpatel:Harsh2005@cluster0.d9fud.mongodb.net/codeforge?retryWrites=true&w=majority&appName=Cluster0",
    "mongodb+srv://harshpatel:Harsh2005@cluster0.d9fud.mongodb.net/codeforge?retryWrites=true&w=majority",
    "mongodb://harshpatel:Harsh2005@cluster0-shard-00-00.d9fud.mongodb.net:27017,cluster0-shard-00-01.d9fud.mongodb.net:27017,cluster0-shard-00-02.d9fud.mongodb.net:27017/codeforge?ssl=true&replicaSet=atlas-123abc-shard-0&authSource=admin&retryWrites=true&w=majority"
]

async def test_motor_connection():
    """Test Motor (async) connection"""
    print("Testing Motor (async) connections...")
    
    for i, url in enumerate(MONGODB_URLS, 1):
        try:
            print(f"\nTrying connection {i}...")
            client = AsyncIOMotorClient(url, serverSelectionTimeoutMS=5000)
            
            # Test the connection
            await client.admin.command('ping')
            print(f"✅ Motor connection {i} successful!")
            
            # Count problems
            db = client.codeforge
            count = await db.problems.count_documents({})
            print(f"Current problems in database: {count}")
            
            client.close()
            return url
            
        except Exception as e:
            print(f"❌ Motor connection {i} failed: {str(e)}")
            
    return None

def test_pymongo_connection():
    """Test PyMongo (sync) connection"""
    print("\nTesting PyMongo (sync) connections...")
    
    for i, url in enumerate(MONGODB_URLS, 1):
        try:
            print(f"\nTrying connection {i}...")
            client = pymongo.MongoClient(url, serverSelectionTimeoutMS=5000)
            
            # Test the connection
            client.admin.command('ping')
            print(f"✅ PyMongo connection {i} successful!")
            
            # Count problems
            db = client.codeforge
            count = db.problems.count_documents({})
            print(f"Current problems in database: {count}")
            
            client.close()
            return url
            
        except Exception as e:
            print(f"❌ PyMongo connection {i} failed: {str(e)}")
            
    return None

async def main():
    print("🔍 Testing MongoDB connections...\n")
    
    # Test Motor
    working_motor_url = await test_motor_connection()
    
    # Test PyMongo  
    working_pymongo_url = test_pymongo_connection()
    
    print(f"\n📊 Results:")
    print(f"Motor working URL: {working_motor_url is not None}")
    print(f"PyMongo working URL: {working_pymongo_url is not None}")
    
    if working_motor_url:
        print(f"\n✅ Use this URL for Motor: {working_motor_url}")
    elif working_pymongo_url:
        print(f"\n✅ Use this URL for PyMongo: {working_pymongo_url}")
    else:
        print(f"\n❌ No working connections found. Check:")
        print("1. Internet connectivity")
        print("2. MongoDB Atlas cluster status")
        print("3. IP whitelist settings")
        print("4. Username/password credentials")

if __name__ == "__main__":
    asyncio.run(main())
