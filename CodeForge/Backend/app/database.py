from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.server_api import ServerApi
import os
from dotenv import load_dotenv

load_dotenv()

class Database:
    client: AsyncIOMotorClient = None
    
database = Database()

async def get_database() -> AsyncIOMotorClient:
    return database.client

async def connect_to_mongo():
    """Create database connection"""
    database.client = AsyncIOMotorClient(
        os.getenv("MONGODB_URL"), 
        server_api=ServerApi('1')
    )
    
async def close_mongo_connection():
    """Close database connection"""
    if database.client:
        database.client.close()

async def get_collection(collection_name: str):
    """Get a specific collection from the database"""
    db = database.client[os.getenv("DATABASE_NAME")]
    return db[collection_name]
