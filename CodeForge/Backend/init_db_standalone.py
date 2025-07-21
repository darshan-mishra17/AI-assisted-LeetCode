"""
Standalone database initialization script for CodeForge
Run this script to populate the database with sample data for testing
"""

import asyncio
import os
import sys
from pathlib import Path
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime
from passlib.context import CryptContext
import re
from dotenv import load_dotenv
from bson import ObjectId

load_dotenv()

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    """Generate password hash"""
    return pwd_context.hash(password)

def create_slug(title: str) -> str:
    """Create URL-friendly slug from title"""
    slug = title.lower()
    slug = re.sub(r'[^\w\s-]', '', slug)
    slug = re.sub(r'[-\s]+', '-', slug)
    return slug.strip('-')

async def init_database():
    """Initialize database with sample data"""
    
    # Connect to MongoDB
    client = AsyncIOMotorClient(os.getenv("MONGODB_URL"))
    db = client[os.getenv("DATABASE_NAME")]
    
    print("🚀 Initializing CodeForge database...")
    
    # Clear existing collections (optional - comment out for production)
    collections = ["users", "problems", "submissions", "discussions", "comments", "roadmaps", "badges"]
    for collection_name in collections:
        await db[collection_name].delete_many({})
        print(f"   Cleared {collection_name} collection")
    
    # Create admin user
    admin_user_data = {
        "_id": ObjectId(),
        "username": "admin",
        "email": "admin@codeforge.dev",
        "full_name": "System Administrator",
        "hashed_password": get_password_hash("admin123"),
        "role": "admin",
        "is_active": True,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
        "avatar_url": None,
        "bio": None,
        "github_url": None,
        "linkedin_url": None,
        "stats": {
            "total_problems_solved": 50,
            "easy_solved": 20,
            "medium_solved": 20,
            "hard_solved": 10,
            "xp": 1000,
            "current_streak": 5,
            "max_streak": 10,
            "last_active": datetime.utcnow()
        },
        "badges": [],
        "solved_problems": [],
        "roadmap_progress": {}
    }
    
    users_collection = db["users"]
    await users_collection.insert_one(admin_user_data)
    print("   ✅ Created admin user (username: admin, password: admin123)")
    
    # Create sample regular user
    sample_user_data = {
        "_id": ObjectId(),
        "username": "johndev",
        "email": "john@example.com",
        "full_name": "John Developer",
        "hashed_password": get_password_hash("password123"),
        "role": "user",
        "is_active": True,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
        "avatar_url": None,
        "bio": "Passionate software developer",
        "github_url": None,
        "linkedin_url": None,
        "stats": {
            "total_problems_solved": 15,
            "easy_solved": 10,
            "medium_solved": 5,
            "hard_solved": 0,
            "xp": 250,
            "current_streak": 3,
            "max_streak": 5,
            "last_active": datetime.utcnow()
        },
        "badges": [],
        "solved_problems": [],
        "roadmap_progress": {}
    }
    
    await users_collection.insert_one(sample_user_data)
    print("   ✅ Created sample user (username: johndev, password: password123)")
    
    # Create sample problems
    problems_data = [
        {
            "_id": ObjectId(),
            "title": "Two Sum",
            "slug": "two-sum",
            "description": """Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.

You may assume that each input would have exactly one solution, and you may not use the same element twice.

You can return the answer in any order.

Example 1:
Input: nums = [2,7,11,15], target = 9
Output: [0,1]
Explanation: Because nums[0] + nums[1] == 9, we return [0, 1].

Example 2:
Input: nums = [3,2,4], target = 6
Output: [1,2]

Example 3:
Input: nums = [3,3], target = 6
Output: [0,1]""",
            "difficulty": "easy",
            "topics": ["Array", "Hash Table"],
            "companies": ["Amazon", "Google", "Apple"],
            "code_templates": {
                "python": """def twoSum(nums, target):
    \"\"\"
    :type nums: List[int]
    :type target: int
    :rtype: List[int]
    \"\"\"
    pass""",
                "java": """class Solution {
    public int[] twoSum(int[] nums, int target) {
        
    }
}""",
                "cpp": """class Solution {
public:
    vector<int> twoSum(vector<int>& nums, int target) {
        
    }
};"""
            },
            "test_cases": [
                {"input": "[2,7,11,15]\\n9", "expected_output": "[0,1]", "is_sample": True, "explanation": None},
                {"input": "[3,2,4]\\n6", "expected_output": "[1,2]", "is_sample": True, "explanation": None},
                {"input": "[3,3]\\n6", "expected_output": "[0,1]", "is_sample": True, "explanation": None},
                {"input": "[1,2,3,4,5]\\n9", "expected_output": "[3,4]", "is_sample": False, "explanation": None},
            ],
            "constraints": [
                "2 <= nums.length <= 10⁴",
                "-10⁹ <= nums[i] <= 10⁹",
                "-10⁹ <= target <= 10⁹",
                "Only one valid answer exists."
            ],
            "hints": [
                "Try using a hash table to store numbers you've seen",
                "For each number, check if target - number exists in your hash table"
            ],
            "created_by": str(admin_user_data["_id"]),
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
            "acceptance_rate": 65.5,
            "total_submissions": 1000,
            "total_accepted": 655
        },
        {
            "_id": ObjectId(),
            "title": "Valid Parentheses",
            "slug": "valid-parentheses",
            "description": """Given a string s containing just the characters '(', ')', '{', '}', '[' and ']', determine if the input string is valid.

An input string is valid if:
1. Open brackets must be closed by the same type of brackets.
2. Open brackets must be closed in the correct order.
3. Every close bracket has a corresponding open bracket of the same type.

Example 1:
Input: s = "()"
Output: true

Example 2:
Input: s = "()[]{}"
Output: true

Example 3:
Input: s = "(]"
Output: false""",
            "difficulty": "easy",
            "topics": ["String", "Stack"],
            "companies": ["Microsoft", "Amazon", "Facebook"],
            "code_templates": {
                "python": """def isValid(s):
    \"\"\"
    :type s: str
    :rtype: bool
    \"\"\"
    pass""",
                "java": """class Solution {
    public boolean isValid(String s) {
        
    }
}"""
            },
            "test_cases": [
                {"input": "()", "expected_output": "true", "is_sample": True, "explanation": None},
                {"input": "()[]{}", "expected_output": "true", "is_sample": True, "explanation": None},
                {"input": "(]", "expected_output": "false", "is_sample": True, "explanation": None},
                {"input": "([)]", "expected_output": "false", "is_sample": False, "explanation": None},
            ],
            "constraints": [
                "1 <= s.length <= 10⁴",
                "s consists of parentheses only '()[]{}'."
            ],
            "hints": [
                "Use a stack to keep track of opening brackets",
                "When you see a closing bracket, check if it matches the most recent opening bracket"
            ],
            "created_by": str(admin_user_data["_id"]),
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
            "acceptance_rate": 72.3,
            "total_submissions": 800,
            "total_accepted": 578
        },
        {
            "_id": ObjectId(),
            "title": "Longest Palindromic Substring",
            "slug": "longest-palindromic-substring",
            "description": """Given a string s, return the longest palindromic substring in s.

A string is called a palindrome string if the reverse of that string is the same as the original string.

Example 1:
Input: s = "babad"
Output: "bab"
Explanation: "aba" is also a valid answer.

Example 2:
Input: s = "cbbd"
Output: "bb"

Example 3:
Input: s = "a"
Output: "a"

Example 4:
Input: s = "ac"
Output: "a" """,
            "difficulty": "medium",
            "topics": ["String", "Dynamic Programming"],
            "companies": ["Amazon", "Microsoft", "Apple"],
            "code_templates": {
                "python": """def longestPalindrome(s):
    \"\"\"
    :type s: str
    :rtype: str
    \"\"\"
    pass""",
                "java": """class Solution {
    public String longestPalindrome(String s) {
        
    }
}"""
            },
            "test_cases": [
                {"input": "babad", "expected_output": "bab", "is_sample": True, "explanation": None},
                {"input": "cbbd", "expected_output": "bb", "is_sample": True, "explanation": None},
                {"input": "a", "expected_output": "a", "is_sample": True, "explanation": None},
                {"input": "ac", "expected_output": "a", "is_sample": True, "explanation": None},
            ],
            "constraints": [
                "1 <= s.length <= 1000",
                "s consist of only digits and English letters."
            ],
            "hints": [
                "Try expanding around centers",
                "Consider both odd and even length palindromes"
            ],
            "created_by": str(admin_user_data["_id"]),
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
            "acceptance_rate": 45.2,
            "total_submissions": 1200,
            "total_accepted": 542
        }
    ]
    
    problems_collection = db["problems"]
    for problem_data in problems_data:
        await problems_collection.insert_one(problem_data)
    
    print(f"   ✅ Created {len(problems_data)} sample problems")
    
    # Create sample roadmap
    roadmap_data = {
        "_id": ObjectId(),
        "title": "Beginner's Programming Journey",
        "description": "A comprehensive roadmap for beginners to learn programming fundamentals through coding problems",
        "difficulty_level": "beginner",
        "estimated_weeks": 8,
        "topics": [
            {
                "id": "basics",
                "title": "Programming Basics",
                "description": "Learn fundamental programming concepts",
                "problems": [str(problems_data[0]["_id"]), str(problems_data[1]["_id"])],
                "prerequisites": []
            },
            {
                "id": "data-structures",
                "title": "Data Structures",
                "description": "Understanding arrays, strings, and basic data structures",
                "problems": [str(problems_data[2]["_id"])],
                "prerequisites": ["basics"]
            }
        ],
        "created_at": datetime.utcnow()
    }
    
    roadmaps_collection = db["roadmaps"]
    await roadmaps_collection.insert_one(roadmap_data)
    print("   ✅ Created sample roadmap")
    
    # Create sample discussion
    discussion_data = {
        "_id": ObjectId(),
        "title": "Tips for solving Two Sum problem efficiently",
        "content": "I've been working on the Two Sum problem and wanted to share some insights. Using a hash map can reduce the time complexity significantly. Here's my approach...",
        "author_id": str(sample_user_data["_id"]),
        "problem_id": str(problems_data[0]["_id"]),
        "upvotes": 5,
        "downvotes": 0,
        "upvoted_by": [],
        "downvoted_by": [],
        "comments_count": 0,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    
    discussions_collection = db["discussions"]
    await discussions_collection.insert_one(discussion_data)
    print("   ✅ Created sample discussion")
    
    # Create sample badges
    badges_data = [
        {
            "_id": ObjectId(),
            "name": "First Steps",
            "description": "Solve your first problem",
            "icon": "🎯",
            "criteria": {"problems_solved": 1}
        },
        {
            "_id": ObjectId(),
            "name": "Getting Started",
            "description": "Solve 5 problems",
            "icon": "🚀",
            "criteria": {"problems_solved": 5}
        },
        {
            "_id": ObjectId(),
            "name": "Problem Solver",
            "description": "Solve 25 problems",
            "icon": "🧠",
            "criteria": {"problems_solved": 25}
        },
        {
            "_id": ObjectId(),
            "name": "Streak Master",
            "description": "Maintain a 7-day streak",
            "icon": "🔥",
            "criteria": {"streak": 7}
        }
    ]
    
    badges_collection = db["badges"]
    for badge in badges_data:
        await badges_collection.insert_one(badge)
    
    print(f"   ✅ Created {len(badges_data)} achievement badges")
    
    # Create indexes for better performance
    await users_collection.create_index("username", unique=True)
    await users_collection.create_index("email", unique=True)
    await problems_collection.create_index("slug", unique=True)
    await problems_collection.create_index([("difficulty", 1), ("topics", 1)])
    await discussions_collection.create_index([("created_at", -1)])
    await discussions_collection.create_index([("upvotes", -1)])
    
    print("   ✅ Created database indexes")
    
    client.close()
    print("🎉 Database initialization completed successfully!")
    print("\\n📋 Summary:")
    print("   • Admin user: admin / admin123")
    print("   • Sample user: johndev / password123")
    print(f"   • {len(problems_data)} coding problems")
    print("   • 1 learning roadmap")
    print("   • 1 sample discussion")
    print(f"   • {len(badges_data)} achievement badges")
    print("\\n🚀 You can now start the FastAPI server!")

if __name__ == "__main__":
    asyncio.run(init_database())
