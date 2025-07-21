import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

async def get_problems():
    client = AsyncIOMotorClient(os.getenv("MONGODB_URI"))
    db = client["codeforge"]
    problems = db["problems"]
    
    # Get all problems
    cursor = problems.find({})
    async for problem in cursor:
        print(f"Title: {problem['title']}")
        print(f"ID: {problem['_id']}")
        print(f"Slug: {problem['slug']}")
        print("---")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(get_problems())
