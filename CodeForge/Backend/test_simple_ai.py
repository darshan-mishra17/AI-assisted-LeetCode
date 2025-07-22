import asyncio
from app.services.simple_ai_mentor import SimpleAIMentor

async def test_simple_ai_mentor():
    """Test the simple AI mentor"""
    
    print("Testing Simple AI Mentor...")
    
    try:
        mentor = SimpleAIMentor()
        print("✅ Simple AI Mentor initialized successfully!")
    except Exception as e:
        print(f"❌ Initialization failed: {e}")
        return
    
    # Test personalized hint
    print("\n1. Testing personalized hint...")
    try:
        hint = await mentor.get_personalized_hint(
            problem_title="Two Sum",
            problem_description="Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.",
            user_code="def twoSum(self, nums, target):\n    # I'm stuck here\n    pass",
            user_level="beginner"
        )
        if hint['confidence'] > 0:
            print(f"✅ Hint generated: {hint['hint'][:200]}...")
        else:
            print(f"❌ Hint failed: {hint['hint']}")
    except Exception as e:
        print(f"❌ Hint generation failed: {e}")
    
    # Test code analysis
    print("\n2. Testing code analysis...")
    try:
        analysis = await mentor.analyze_user_code(
            code="def twoSum(nums, target):\n    for i in range(len(nums)):\n        for j in range(i+1, len(nums)):\n            if nums[i] + nums[j] == target:\n                return [i, j]",
            problem_context="Two Sum problem"
        )
        if analysis['success']:
            print(f"✅ Analysis generated: {analysis['analysis'][:200]}...")
        else:
            print(f"❌ Analysis failed: {analysis['analysis']}")
    except Exception as e:
        print(f"❌ Code analysis failed: {e}")
    
    # Test concept explanation
    print("\n3. Testing concept explanation...")
    try:
        explanation = await mentor.explain_concept(
            concept="Hash Tables",
            context="Used for solving Two Sum problem efficiently"
        )
        print(f"✅ Explanation generated: {explanation['explanation'][:200]}...")
    except Exception as e:
        print(f"❌ Concept explanation failed: {e}")
    
    # Test mentor status
    print("\n4. Testing mentor status...")
    try:
        status = await mentor.get_mentor_status()
        print(f"✅ Status: {status['status']} - Capabilities: {len(status['capabilities'])}")
    except Exception as e:
        print(f"❌ Status check failed: {e}")
    
    print("\n🎉 Simple AI Mentor test completed!")

if __name__ == "__main__":
    asyncio.run(test_simple_ai_mentor())
