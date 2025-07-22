import os
import asyncio
import json
from typing import Dict, List, Optional
from datetime import datetime
import httpx
from dotenv import load_dotenv

load_dotenv()

class SimpleAIMentor:
    """Simple AI Mentor using direct Groq API calls"""
    
    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("GROQ_API_KEY environment variable is required")
        
        self.base_url = "https://api.groq.com/openai/v1/chat/completions"
        self.model = "llama-3.1-8b-instant"  # Using currently available model
        
        print("✅ Simple AI Mentor initialized")
    
    async def _make_api_call(self, messages: List[Dict], max_tokens: int = 1000) -> str:
        """Make a direct API call to Groq"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.model,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": 0.1
        }
        
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                self.base_url,
                headers=headers,
                json=payload
            )
            
            if response.status_code != 200:
                error_text = response.text
                print(f"API Error Details: {response.status_code} - {error_text}")
                raise Exception(f"API call failed: {response.status_code} - {error_text}")
            
            result = response.json()
            return result["choices"][0]["message"]["content"]
    
    async def get_personalized_hint(
        self, 
        problem_title: str, 
        problem_description: str, 
        user_code: str, 
        user_level: str = "beginner"
    ) -> Dict:
        """Generate a personalized hint for the user"""
        
        messages = [
            {
                "role": "system",
                "content": f"You are an expert coding mentor helping a {user_level} programmer. Provide helpful, personalized hints without giving away the complete solution."
            },
            {
                "role": "user", 
                "content": f"""
Problem: {problem_title}
Description: {problem_description}

Current code attempt:
{user_code}

Please provide a helpful hint that guides me toward the solution without revealing it completely. Consider my {user_level} level.
"""
            }
        ]
        
        try:
            hint_text = await self._make_api_call(messages)
            return {
                "hint": hint_text,
                "confidence": 0.9,
                "personalized": True,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            return {
                "hint": f"I'm having trouble generating a hint right now. Error: {str(e)}",
                "confidence": 0.0,
                "personalized": False,
                "timestamp": datetime.now().isoformat()
            }
    
    async def analyze_user_code(self, code: str, problem_context: str) -> Dict:
        """Analyze user's code and provide feedback"""
        
        messages = [
            {
                "role": "system",
                "content": "You are an expert code reviewer. Analyze the provided code and give constructive feedback on logic, efficiency, and potential improvements."
            },
            {
                "role": "user",
                "content": f"""
Problem Context: {problem_context}

Code to analyze:
{code}

Please analyze this code and provide feedback on:
1. Logic correctness
2. Time/space complexity
3. Potential improvements
4. Edge cases to consider
"""
            }
        ]
        
        try:
            analysis_text = await self._make_api_call(messages)
            return {
                "analysis": analysis_text,
                "timestamp": datetime.now().isoformat(),
                "success": True
            }
        except Exception as e:
            return {
                "analysis": f"Unable to analyze code at the moment. Error: {str(e)}",
                "timestamp": datetime.now().isoformat(),
                "success": False
            }
    
    async def explain_concept(self, concept: str, context: str = "") -> Dict:
        """Explain a programming concept"""
        
        messages = [
            {
                "role": "system",
                "content": "You are an expert programming teacher. Explain concepts clearly with examples."
            },
            {
                "role": "user",
                "content": f"""
Please explain the concept: {concept}
{f"Context: {context}" if context else ""}

Provide a clear explanation with:
1. Definition
2. How it works
3. When to use it
4. Simple example
"""
            }
        ]
        
        try:
            explanation = await self._make_api_call(messages)
            return {
                "explanation": explanation,
                "concept": concept,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            return {
                "explanation": f"Unable to explain concept right now. Error: {str(e)}",
                "concept": concept,
                "timestamp": datetime.now().isoformat()
            }
    
    async def get_learning_path(self, current_skills: List[str], target_goal: str) -> Dict:
        """Generate a personalized learning path"""
        
        messages = [
            {
                "role": "system",
                "content": "You are a programming education expert. Create personalized learning paths."
            },
            {
                "role": "user",
                "content": f"""
Current skills: {', '.join(current_skills)}
Target goal: {target_goal}

Please create a step-by-step learning path with:
1. Skills to develop
2. Recommended practice problems
3. Timeline suggestions
4. Resources to study
"""
            }
        ]
        
        try:
            path_text = await self._make_api_call(messages, max_tokens=1500)
            return {
                "learning_path": path_text,
                "current_skills": current_skills,
                "target_goal": target_goal,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            return {
                "learning_path": f"Unable to generate learning path. Error: {str(e)}",
                "current_skills": current_skills,
                "target_goal": target_goal,
                "timestamp": datetime.now().isoformat()
            }
    
    async def debug_code(self, code: str, error_message: str, expected_behavior: str) -> Dict:
        """Help debug code issues"""
        
        messages = [
            {
                "role": "system",
                "content": "You are an expert debugger. Help identify and fix code issues."
            },
            {
                "role": "user",
                "content": f"""
Code with issues:
{code}

Error message: {error_message}
Expected behavior: {expected_behavior}

Please help me debug this by:
1. Identifying the issue
2. Explaining why it happens
3. Suggesting a fix
4. Providing corrected code if needed
"""
            }
        ]
        
        try:
            debug_info = await self._make_api_call(messages, max_tokens=1500)
            return {
                "debug_suggestions": debug_info,
                "error_message": error_message,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            return {
                "debug_suggestions": f"Unable to debug code right now. Error: {str(e)}",
                "error_message": error_message,
                "timestamp": datetime.now().isoformat()
            }
    
    async def get_mentor_status(self) -> Dict:
        """Get the status of the AI mentor"""
        return {
            "status": "active",
            "model": self.model,
            "capabilities": [
                "personalized_hints",
                "code_analysis",
                "concept_explanation",
                "debugging_help",
                "learning_paths"
            ],
            "last_updated": datetime.now().isoformat()
        }
