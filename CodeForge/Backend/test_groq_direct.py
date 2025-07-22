import os
from dotenv import load_dotenv
import groq

# Load environment variables
load_dotenv()

def test_groq_direct():
    """Test Groq client directly"""
    
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("❌ GROQ_API_KEY not found")
        return
    
    print(f"✅ API Key found: {api_key[:10]}...")
    
    try:
        # Test direct Groq client
        client = groq.Groq(api_key=api_key)
        print("✅ Direct Groq client initialized successfully!")
        
        # Test a simple completion
        response = client.chat.completions.create(
            model="mixtral-8x7b-32768",
            messages=[{"role": "user", "content": "Say hello"}],
            max_tokens=50
        )
        print(f"✅ API call successful: {response.choices[0].message.content}")
        
    except Exception as e:
        print(f"❌ Direct Groq client failed: {e}")

if __name__ == "__main__":
    test_groq_direct()
