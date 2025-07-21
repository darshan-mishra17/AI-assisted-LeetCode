#!/usr/bin/env python3
"""
Script to check how many problems are in the database
"""

import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

# MongoDB connection
MONGODB_URL = "mongodb+srv://harshpatel:Harsh2005@cluster0.d9fud.mongodb.net/codeforge?retryWrites=true&w=majority&appName=Cluster0"

async def check_problems():
    """Check problems in the MongoDB database"""
    try:
        # Connect to MongoDB
        client = AsyncIOMotorClient(MONGODB_URL)
        db = client.codeforge
        problems_collection = db.problems
        
        # Count problems
        total_problems = await problems_collection.count_documents({})
        easy_count = await problems_collection.count_documents({"difficulty": "easy"})
        medium_count = await problems_collection.count_documents({"difficulty": "medium"}) 
        hard_count = await problems_collection.count_documents({"difficulty": "hard"})
        
        print(f"Database Summary:")
        print(f"Total problems: {total_problems}")
        print(f"Easy: {easy_count}")
        print(f"Medium: {medium_count}")
        print(f"Hard: {hard_count}")
        
        # Show first few problem titles
        print(f"\nFirst 10 problems:")
        problems = await problems_collection.find({}).limit(10).to_list(10)
        for i, problem in enumerate(problems, 1):
            print(f"{i}. {problem['title']} ({problem['difficulty']})")
        
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        client.close()

if __name__ == "__main__":
    asyncio.run(check_problems())
