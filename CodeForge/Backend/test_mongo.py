"""
Test MongoDB connection
"""

import asyncio
import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

async def test_connection():
    """Test MongoDB connection"""
    mongodb_url = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
    
    print(f"Testing connection to: {mongodb_url}")
    
    try:
        client = AsyncIOMotorClient(mongodb_url)
        
        # Test the connection
        await client.admin.command('ping')
        print("✅ MongoDB connection successful!")
        
        # List databases
        db_list = await client.list_database_names()
        print(f"Available databases: {db_list}")
        
        # Test database access
        db_name = os.getenv("DATABASE_NAME", "codeforge")
        db = client[db_name]
        collections = await db.list_collection_names()
        print(f"Collections in '{db_name}': {collections}")
        
        client.close()
        return True
        
    except Exception as e:
        print(f"❌ MongoDB connection failed: {e}")
        print("\n💡 Solutions:")
        print("1. Install MongoDB locally: https://www.mongodb.com/try/download/community")
        print("2. Use MongoDB Atlas (cloud): https://www.mongodb.com/cloud/atlas")
        print("3. Use Docker: docker run -d -p 27017:27017 mongo:6.0")
        print("4. Check MONGODB_URL in your .env file")
        return False

if __name__ == "__main__":
    asyncio.run(test_connection())
