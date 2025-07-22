#!/usr/bin/env python3
"""
Test script for Advanced AI Mentor system
"""

import asyncio
import sys
import os
from pathlib import Path

# Add the app directory to Python path
app_dir = Path(__file__).parent / "app"
sys.path.insert(0, str(app_dir))

async def test_ai_mentor():
    print("🤖 Testing Advanced AI Mentor System...")
    print("=" * 50)
    
    try:
        # Test 1: Import the advanced AI mentor service
        print("📦 Testing imports...")
        from services.advanced_ai_mentor import AdvancedAIMentor
        print("✅ Advanced AI Mentor import successful")
        
        # Test 2: Check environment variables
        print("\n🔧 Checking environment variables...")
        groq_key = os.getenv("GROQ_API_KEY")
        if groq_key and not groq_key.startswith("your_"):
            print("✅ GROQ_API_KEY is configured")
        else:
            print("⚠️ GROQ_API_KEY not properly configured")
            
        chromadb_path = os.getenv("CHROMADB_PATH", "./chroma_db")
        if os.path.exists(chromadb_path):
            print("✅ ChromaDB directory exists")
        else:
            print("⚠️ ChromaDB directory not found")
        
        # Test 3: Initialize AI Mentor
        print("\n🚀 Initializing AI Mentor...")
        if groq_key and not groq_key.startswith("your_"):
            ai_mentor = AdvancedAIMentor()
            print("✅ AI Mentor initialized successfully")
            
            # Test 4: Test a simple hint request
            print("\n💡 Testing hint generation...")
            result = await ai_mentor.get_personalized_hint(
                problem_description="Given an array of integers and a target, find two numbers that add up to target",
                user_code="def two_sum(nums, target):\n    pass",
                language="python",
                user_id="test_user",
                hint_level="gentle"
            )
            
            print("✅ Hint generation successful")
            print(f"Hint preview: {result['hint'][:100]}...")
            print(f"Confidence: {result['confidence_score']}")
            print(f"Next steps: {len(result['suggested_next_steps'])} suggestions")
            
        else:
            print("⚠️ Skipping AI Mentor initialization (API key not configured)")
            
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure all dependencies are installed:")
        print("pip install langchain langchain-community langchain-groq chromadb sentence-transformers")
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        print("Check your configuration and try again")
        
    print("\n" + "=" * 50)
    print("🎉 AI Mentor test completed!")

if __name__ == "__main__":
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    # Run the test
    asyncio.run(test_ai_mentor())
