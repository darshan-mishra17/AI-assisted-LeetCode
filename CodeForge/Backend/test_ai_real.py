import asyncio
import os
from dotenv import load_dotenv
from app.services.advanced_ai_mentor import AdvancedAIMentor

# Load environment variables
load_dotenv()

async def test_ai_mentor():
    """Test the AI mentor with real API calls"""
    
    # Initialize the AI mentor
    mentor = AdvancedAIMentor()
    
    print("Testing AI Mentor Initialization...")
    try:
        await mentor.initialize()
        print("✅ AI Mentor initialized successfully!")
    except Exception as e:
        print(f"❌ Initialization failed: {e}")
        return
    
    # Test personalized hint
    print("\nTesting personalized hint...")
    try:
        hint = await mentor.get_personalized_hint(
            problem_title="Two Sum",
            problem_description="Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.",
            user_code="def twoSum(self, nums, target):\n    # I'm stuck here\n    pass",
            user_level="beginner"
        )
        print(f"✅ Hint generated: {hint['hint'][:100]}...")
    except Exception as e:
        print(f"❌ Hint generation failed: {e}")
    
    # Test code analysis
    print("\nTesting code analysis...")
    try:
        analysis = await mentor.analyze_user_code(
            code="def twoSum(nums, target):\n    for i in range(len(nums)):\n        for j in range(i+1, len(nums)):\n            if nums[i] + nums[j] == target:\n                return [i, j]",
            problem_context="Two Sum problem"
        )
        print(f"✅ Analysis generated: {analysis['analysis'][:100]}...")
    except Exception as e:
        print(f"❌ Code analysis failed: {e}")
    
    print("\nAI Mentor test completed!")

if __name__ == "__main__":
    asyncio.run(test_ai_mentor())
