"""
Database initialization script for CodeForge
Run this script to populate the database with sample data for testing
"""

import asyncio
import os
import sys
from pathlib import Path

# Add the app directory to Python path
current_dir = Path(__file__).resolve().parent
app_dir = current_dir / "app"
sys.path.append(str(app_dir))

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
    admin_user = User(
        username="admin",
        email="admin@codeforge.dev",
        full_name="System Administrator",
        hashed_password=get_password_hash("admin123"),
        role="admin",
        stats=UserStats(xp=1000, total_problems_solved=50)
    )
    
    users_collection = db["users"]
    await users_collection.insert_one(admin_user.dict(by_alias=True))
    print("   ✅ Created admin user (username: admin, password: admin123)")
    
    # Create sample regular user
    sample_user = User(
        username="johndev",
        email="john@example.com",
        full_name="John Developer",
        hashed_password=get_password_hash("password123"),
        role="user",
        bio="Passionate software developer",
        stats=UserStats(xp=250, total_problems_solved=15, current_streak=3)
    )
    
    await users_collection.insert_one(sample_user.dict(by_alias=True))
    print("   ✅ Created sample user (username: johndev, password: password123)")
    
    # Create sample problems
    problems = [
        {
            "title": "Two Sum",
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
            "difficulty": ProblemDifficulty.EASY,
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
                TestCase(input="[2,7,11,15]\n9", expected_output="[0,1]", is_sample=True),
                TestCase(input="[3,2,4]\n6", expected_output="[1,2]", is_sample=True),
                TestCase(input="[3,3]\n6", expected_output="[0,1]", is_sample=True),
                TestCase(input="[1,2,3,4,5]\n9", expected_output="[3,4]", is_sample=False),
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
            ]
        },
        {
            "title": "Valid Parentheses",
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
            "difficulty": ProblemDifficulty.EASY,
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
                TestCase(input="()", expected_output="true", is_sample=True),
                TestCase(input="()[]{}", expected_output="true", is_sample=True),
                TestCase(input="(]", expected_output="false", is_sample=True),
                TestCase(input="([)]", expected_output="false", is_sample=False),
            ],
            "constraints": [
                "1 <= s.length <= 10⁴",
                "s consists of parentheses only '()[]{}'."
            ],
            "hints": [
                "Use a stack to keep track of opening brackets",
                "When you see a closing bracket, check if it matches the most recent opening bracket"
            ]
        },
        {
            "title": "Longest Palindromic Substring",
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
            "difficulty": ProblemDifficulty.MEDIUM,
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
                TestCase(input="babad", expected_output="bab", is_sample=True),
                TestCase(input="cbbd", expected_output="bb", is_sample=True),
                TestCase(input="a", expected_output="a", is_sample=True),
                TestCase(input="ac", expected_output="a", is_sample=True),
            ],
            "constraints": [
                "1 <= s.length <= 1000",
                "s consist of only digits and English letters."
            ],
            "hints": [
                "Try expanding around centers",
                "Consider both odd and even length palindromes"
            ]
        }
    ]
    
    problems_collection = db["problems"]
    for problem_data in problems:
        slug = create_slug(problem_data["title"])
        problem = Problem(
            title=problem_data["title"],
            slug=slug,
            description=problem_data["description"],
            difficulty=problem_data["difficulty"],
            topics=problem_data["topics"],
            companies=problem_data["companies"],
            code_templates=problem_data["code_templates"],
            test_cases=problem_data["test_cases"],
            constraints=problem_data["constraints"],
            hints=problem_data["hints"],
            created_by=str(admin_user.id),
            acceptance_rate=65.5,
            total_submissions=1000,
            total_accepted=655
        )
        await problems_collection.insert_one(problem.dict(by_alias=True))
    
    print(f"   ✅ Created {len(problems)} sample problems")
    
    # Create sample roadmap
    beginner_roadmap = Roadmap(
        title="Beginner's Programming Journey",
        description="A comprehensive roadmap for beginners to learn programming fundamentals through coding problems",
        difficulty_level="beginner",
        estimated_weeks=8,
        topics=[
            RoadmapTopic(
                id="basics",
                title="Programming Basics",
                description="Learn fundamental programming concepts",
                problems=[str(p["_id"]) for p in await problems_collection.find({}).to_list(length=2)],
                prerequisites=[]
            ),
            RoadmapTopic(
                id="data-structures",
                title="Data Structures",
                description="Understanding arrays, strings, and basic data structures",
                problems=[str(p["_id"]) for p in await problems_collection.find({}).to_list(length=1)],
                prerequisites=["basics"]
            )
        ]
    )
    
    roadmaps_collection = db["roadmaps"]
    await roadmaps_collection.insert_one(beginner_roadmap.dict(by_alias=True))
    print("   ✅ Created sample roadmap")
    
    # Create sample discussion
    discussion = Discussion(
        title="Tips for solving Two Sum problem efficiently",
        content="I've been working on the Two Sum problem and wanted to share some insights. Using a hash map can reduce the time complexity significantly. Here's my approach...",
        author_id=str(sample_user.id),
        problem_id=str(list(await problems_collection.find({"title": "Two Sum"}).to_list(length=1))[0]["_id"]),
        upvotes=5,
        comments_count=0
    )
    
    discussions_collection = db["discussions"]
    discussion_result = await discussions_collection.insert_one(discussion.dict(by_alias=True))
    print("   ✅ Created sample discussion")
    
    # Create sample badges
    badges = [
        Badge(
            name="First Steps",
            description="Solve your first problem",
            icon="🎯",
            criteria={"problems_solved": 1}
        ),
        Badge(
            name="Getting Started",
            description="Solve 5 problems",
            icon="🚀",
            criteria={"problems_solved": 5}
        ),
        Badge(
            name="Problem Solver",
            description="Solve 25 problems",
            icon="🧠",
            criteria={"problems_solved": 25}
        ),
        Badge(
            name="Streak Master",
            description="Maintain a 7-day streak",
            icon="🔥",
            criteria={"streak": 7}
        )
    ]
    
    badges_collection = db["badges"]
    for badge in badges:
        await badges_collection.insert_one(badge.dict(by_alias=True))
    
    print(f"   ✅ Created {len(badges)} achievement badges")
    
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
    print("\n📋 Summary:")
    print("   • Admin user: admin / admin123")
    print("   • Sample user: johndev / password123")
    print(f"   • {len(problems)} coding problems")
    print("   • 1 learning roadmap")
    print("   • 1 sample discussion")
    print(f"   • {len(badges)} achievement badges")
    print("\n🚀 You can now start the FastAPI server!")

if __name__ == "__main__":
    asyncio.run(init_database())
