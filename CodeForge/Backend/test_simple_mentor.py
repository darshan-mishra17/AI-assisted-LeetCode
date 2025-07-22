import asyncio
from dotenv import load_dotenv
from app.services.simple_ai_mentor import SimpleAIMentor

load_dotenv()

async def test_simple_mentor():
    mentor = SimpleAIMentor()
    
    print("Testing hint generation...")
    result = await mentor.get_personalized_hint(
        problem_title="Two Sum",
        problem_description="Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.",
        user_code="def twoSum(self, nums, target):\n    # I'm stuck here\n    pass",
        user_level="beginner"
    )
    
    print(f"✅ Hint: {result['hint'][:100]}...")
    print(f"Confidence: {result['confidence']}")
    print(f"Personalized: {result['personalized']}")

if __name__ == "__main__":
    asyncio.run(test_simple_mentor())
