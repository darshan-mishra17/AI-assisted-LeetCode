#!/usr/bin/env python3
"""
Quick test to add problems and verify the API
"""

import asyncio
import requests
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient

# MongoDB connection
MONGODB_URL = "mongodb+srv://harshpatel:Harsh2005@cluster0.d9fud.mongodb.net/codeforge?retryWrites=true&w=majority&appName=Cluster0"

# Define some basic problems to add
basic_problems = [
    {
        "title": "Reverse Integer",
        "slug": "reverse-integer",
        "difficulty": "easy",
        "description": "Given a signed 32-bit integer x, return x with its digits reversed.",
        "examples": [{"input": "x = 123", "output": "321"}],
        "constraints": ["-2^31 <= x <= 2^31 - 1"],
        "tags": ["Math"],
        "acceptance_rate": 25.6,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "title": "Palindrome Number",
        "slug": "palindrome-number", 
        "difficulty": "easy",
        "description": "Given an integer x, return true if x is palindrome integer.",
        "examples": [{"input": "x = 121", "output": "true"}],
        "constraints": ["-2^31 <= x <= 2^31 - 1"],
        "tags": ["Math"],
        "acceptance_rate": 49.6,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "title": "Add Two Numbers",
        "slug": "add-two-numbers",
        "difficulty": "medium",
        "description": "Add two numbers represented as linked lists.",
        "examples": [{"input": "l1 = [2,4,3], l2 = [5,6,4]", "output": "[7,0,8]"}],
        "constraints": ["The number of nodes in each linked list is in the range [1, 100]"],
        "tags": ["Linked List", "Math"],
        "acceptance_rate": 36.9,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "title": "Median of Two Sorted Arrays",
        "slug": "median-of-two-sorted-arrays",
        "difficulty": "hard",
        "description": "Given two sorted arrays, return the median of the two sorted arrays.",
        "examples": [{"input": "nums1 = [1,3], nums2 = [2]", "output": "2.00000"}],
        "constraints": ["nums1.length == m", "nums2.length == n"],
        "tags": ["Array", "Binary Search"],
        "acceptance_rate": 35.4,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
]

async def add_basic_problems():
    """Add basic problems to ensure we have more than 3"""
    try:
        client = AsyncIOMotorClient(MONGODB_URL)
        db = client.codeforge
        problems_collection = db.problems
        
        # Check current count
        current_count = await problems_collection.count_documents({})
        print(f"Current problems in database: {current_count}")
        
        if current_count < 10:  # Add more if we have fewer than 10
            print("Adding more problems...")
            result = await problems_collection.insert_many(basic_problems)
            print(f"Added {len(result.inserted_ids)} problems")
            
            # Check new count
            new_count = await problems_collection.count_documents({})
            print(f"New total problems: {new_count}")
        else:
            print("Database already has enough problems")
            
        # Show breakdown by difficulty
        easy = await problems_collection.count_documents({"difficulty": "easy"})
        medium = await problems_collection.count_documents({"difficulty": "medium"})
        hard = await problems_collection.count_documents({"difficulty": "hard"})
        
        print(f"\nBreakdown:")
        print(f"Easy: {easy}")
        print(f"Medium: {medium}")  
        print(f"Hard: {hard}")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.close()

def test_api():
    """Test the API endpoint"""
    try:
        response = requests.get("http://127.0.0.1:8000/problems?skip=0&limit=100")
        if response.status_code == 200:
            problems = response.json()
            print(f"\nAPI Response: Found {len(problems)} problems via API")
            return True
        else:
            print(f"API Error: {response.status_code}")
            return False
    except Exception as e:
        print(f"API connection error: {e}")
        return False

if __name__ == "__main__":
    print("Adding problems to database...")
    asyncio.run(add_basic_problems())
    
    print("\nTesting API...")
    test_api()
