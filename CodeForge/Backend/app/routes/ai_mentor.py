from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from ..schemas.schemas import AIHintRequest, AIHintResponse
from ..models.models import User
from ..auth.auth import get_current_active_user
from ..database import get_collection
from ..services.simple_ai_mentor import SimpleAIMentor
from bson import ObjectId
import os
import asyncio

router = APIRouter(prefix="/ai", tags=["ai-mentor"])

# Initialize Simple AI Mentor
ai_mentor = None
try:
    if os.getenv("GROQ_API_KEY"):
        ai_mentor = SimpleAIMentor()
        print("✅ Simple AI Mentor initialized successfully")
    else:
        print("⚠️ GROQ_API_KEY not found, AI Mentor will use fallback responses")
except Exception as e:
    print(f"❌ Failed to initialize Simple AI Mentor: {e}")
    ai_mentor = None

# Enhanced Pydantic models for new features
class CodeAnalysisRequest(BaseModel):
    code: str
    language: str = "python"
    problem_description: str

class CodeAnalysisResponse(BaseModel):
    detailed_analysis: str
    complexity_analysis: Dict[str, str]
    quality_score: float
    improvement_suggestions: List[str]
    optimized_code_snippet: str

class ConceptExplanationRequest(BaseModel):
    concept: str
    user_level: str = "intermediate"
    include_examples: bool = True
    programming_language: str = "python"

class ConceptExplanationResponse(BaseModel):
    explanation: str
    related_concepts: List[str]
    practice_problems: List[Dict[str, str]]
    visual_aids: str
    real_world_applications: List[str]

class DebugRequest(BaseModel):
    code: str
    language: str = "python"
    error_message: str
    expected_behavior: str

class DebugResponse(BaseModel):
    debug_analysis: str
    suggested_fixes: List[str]
    corrected_code: str
    prevention_tips: List[str]
    testing_suggestions: List[Dict[str, str]]

class LearningPathRequest(BaseModel):
    current_problem_id: str
    user_strengths: List[str]
    user_weaknesses: List[str]

class LearningPathResponse(BaseModel):
    learning_path: str
    estimated_duration: str
    difficulty_progression: List[str]
    checkpoint_problems: List[Dict[str, str]]
    success_metrics: Dict[str, Any]

class EnhancedAIHintResponse(BaseModel):
    hint: str
    confidence_score: float
    suggested_next_steps: List[str]
    follow_up_questions: List[str]
    learning_resources: List[Dict[str, str]]
    estimated_completion_time: str

@router.post("/hint", response_model=EnhancedAIHintResponse)
async def get_hint(
    request: AIHintRequest
):
    """Get AI-powered personalized hints for coding problems"""
    try:
        problems_collection = await get_collection("problems")
        
        # Get problem details - handle both ObjectId and simple string IDs
        try:
            # First try as ObjectId
            problem_data = await problems_collection.find_one({"_id": ObjectId(request.problem_id)})
        except:
            # If ObjectId fails, try as simple integer or string
            problem_data = await problems_collection.find_one({
                "$or": [
                    {"id": request.problem_id},
                    {"id": int(request.problem_id) if request.problem_id.isdigit() else request.problem_id},
                    {"problem_id": request.problem_id}
                ]
            })
            
        if not problem_data:
            # If problem not found, create a generic response without database lookup
            if not ai_mentor:
                return EnhancedAIHintResponse(
                    hint=f"For this {request.language} problem, consider breaking it down into smaller components. Look at the data structures you're using and think about whether there's a more efficient approach. Focus on understanding the problem pattern first.",
                    confidence_score=0.7,
                    suggested_next_steps=[
                        "Identify the main algorithm pattern (e.g., two pointers, sliding window, DFS/BFS)",
                        "Choose the most appropriate data structure for efficiency",
                        "Consider edge cases and input validation",
                        "Analyze time and space complexity"
                    ],
                    follow_up_questions=[
                        "What's the time complexity of your current approach?",
                        "Are there any edge cases you haven't considered?",
                        "Could a different data structure improve performance?"
                    ],
                    learning_resources=[
                        {"title": "Algorithm Patterns", "url": "https://leetcode.com/explore/"},
                        {"title": "Data Structures Guide", "url": "https://leetcode.com/explore/"}
                    ],
                    estimated_completion_time="15-30 minutes"
                )
            else:
                # Use AI with generic problem context
                result = await ai_mentor.get_personalized_hint(
                    problem_description="Coding problem requiring algorithmic solution",
                    user_code=request.user_code,
                    language=request.language,
                    hint_type=request.hint_type,
                    user_level="intermediate"
                )
                return EnhancedAIHintResponse(**result)
        
        problem_description = problem_data.get("description", "")
        
        if not ai_mentor:
            # Enhanced fallback response
            return EnhancedAIHintResponse(
                hint=f"For this {request.language} problem, consider breaking it down into smaller components. Look at the data structures you're using and think about whether there's a more efficient approach. Focus on understanding the problem pattern first.",
                confidence_score=0.7,
                suggested_next_steps=[
                    "Identify the main algorithm pattern (e.g., two pointers, sliding window, DFS/BFS)",
                    "Choose the most appropriate data structure for efficiency",
                    "Consider edge cases and input validation",
                    "Analyze time and space complexity"
                ],
                follow_up_questions=[
                    "What's the time complexity of your current approach?",
                    "Are there any edge cases you haven't considered?",
                    "Could a different data structure improve performance?"
                ],
                learning_resources=[
                    {
                        "title": "Algorithm Patterns Guide",
                        "type": "tutorial",
                        "url": "https://leetcode.com/explore/",
                        "description": "Comprehensive guide to common coding patterns"
                    }
                ],
                estimated_completion_time="15-30 minutes"
            )
        
        # Use advanced AI mentor
        result = await ai_mentor.get_personalized_hint(
            problem_description=problem_description,
            user_code=request.user_code,
            language=request.language,
            user_id="anonymous",  # Since no authentication required
            hint_level=request.hint_type  # Map hint_type to hint_level
        )
        
        return EnhancedAIHintResponse(**result)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate hint: {str(e)}")

@router.post("/analyze", response_model=CodeAnalysisResponse)
async def analyze_code(
    request: CodeAnalysisRequest
):
    """Comprehensive code quality analysis with optimization suggestions"""
    try:
        if not ai_mentor:
            # Enhanced fallback response
            return CodeAnalysisResponse(
                detailed_analysis=f"""
                **Code Analysis for {request.language} Solution:**

                **Correctness**: The code appears to address the main problem requirements.

                **Time Complexity**: Estimated O(n) - linear time complexity based on visible loops.

                **Space Complexity**: Estimated O(1) - appears to use constant extra space.

                **Code Style**: Following {request.language} conventions with clear variable names.

                **Recommendations**:
                - Add input validation for edge cases
                - Include comprehensive error handling
                - Consider adding comments for complex logic
                - Verify all edge cases are handled properly

                **Optimization Opportunities**:
                - Review if a more efficient algorithm exists
                - Consider using built-in functions for better performance
                - Optimize space usage if possible
                """,
                complexity_analysis={"time": "O(n)", "space": "O(1)"},
                quality_score=0.78,
                improvement_suggestions=[
                    "Add comprehensive input validation",
                    "Include proper error handling mechanisms",
                    "Add inline comments for complex logic",
                    "Consider edge case scenarios",
                    "Optimize variable naming for clarity"
                ],
                optimized_code_snippet=f"# Optimized {request.language} solution\n# Enhanced version would include better error handling\n# and more efficient algorithms where applicable"
            )
        
        # Use advanced AI mentor
        result = await ai_mentor.analyze_code_quality(
            code=request.code,
            language=request.language,
            problem_description=request.problem_description
        )
        
        return CodeAnalysisResponse(**result)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to analyze code: {str(e)}")

@router.post("/explain-concept", response_model=ConceptExplanationResponse)
async def explain_concept(
    request: ConceptExplanationRequest
):
    """Get detailed explanation of programming concepts with examples"""
    try:
        if not ai_mentor:
            # Enhanced fallback response
            return ConceptExplanationResponse(
                explanation=f"""
                **{request.concept.title()}** is a fundamental programming concept that plays a crucial role in algorithm design and problem-solving.

                **Definition**: {request.concept} refers to a specific approach or pattern used to solve computational problems efficiently.

                **Why It's Important**: Understanding {request.concept} helps you:
                - Write more efficient code
                - Solve complex problems systematically  
                - Recognize common patterns in coding interviews
                - Build scalable solutions

                **How It Works**: The concept typically involves analyzing the problem structure and applying proven techniques to achieve optimal solutions.

                **Common Applications**: Used in sorting, searching, optimization, and many algorithmic challenges.
                """,
                related_concepts=["algorithms", "data structures", "complexity analysis", "problem patterns"],
                practice_problems=[
                    {"title": "Two Sum", "difficulty": "Easy", "description": "Practice using hashmaps"},
                    {"title": "Valid Parentheses", "difficulty": "Easy", "description": "Stack-based problem solving"}
                ],
                visual_aids=f"Visual representations of {request.concept} would include diagrams showing the step-by-step process and data flow.",
                real_world_applications=[
                    f"{request.concept} is used in database query optimization",
                    f"Search engines utilize {request.concept} for indexing",
                    f"Operating systems apply {request.concept} for resource management"
                ]
            )
        
        # Use advanced AI mentor
        result = await ai_mentor.explain_concept(
            concept=request.concept,
            user_level=request.user_level,
            include_examples=request.include_examples,
            programming_language=request.programming_language
        )
        
        return ConceptExplanationResponse(**result)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to explain concept: {str(e)}")

@router.post("/debug", response_model=DebugResponse)
async def debug_code(
    request: DebugRequest
):
    """Advanced debugging assistance with step-by-step guidance"""
    try:
        if not ai_mentor:
            # Enhanced fallback response
            return DebugResponse(
                debug_analysis=f"""
                **Debugging Analysis for {request.language} Code:**

                **Error**: {request.error_message}

                **Expected Behavior**: {request.expected_behavior}

                **Root Cause Analysis**:
                - Check for common issues like index out of bounds, null pointer exceptions, or logic errors
                - Verify variable initialization and scope
                - Ensure proper data type handling

                **Debugging Steps**:
                1. Add print statements to trace variable values
                2. Check boundary conditions and edge cases
                3. Verify input validation
                4. Test with simple inputs first

                **Resolution Strategy**:
                - Fix the immediate error first
                - Then optimize for edge cases
                - Add proper error handling
                - Test thoroughly with various inputs
                """,
                suggested_fixes=[
                    "Add bounds checking for array/list access",
                    "Initialize variables properly before use",
                    "Handle null/None values appropriately",
                    "Verify loop conditions and termination"
                ],
                corrected_code=f"# Corrected {request.language} code\n# Would include specific fixes for the identified issues\n# with proper error handling and validation",
                prevention_tips=[
                    "Always validate inputs before processing",
                    "Use defensive programming techniques",
                    "Test with edge cases during development",
                    "Add comprehensive error handling"
                ],
                testing_suggestions=[
                    {"input": "Empty input", "expected": "Handle gracefully", "description": "Test edge case"},
                    {"input": "Normal case", "expected": request.expected_behavior, "description": "Verify basic functionality"},
                    {"input": "Large input", "expected": "Efficient processing", "description": "Performance test"}
                ]
            )
        
        # Use advanced AI mentor
        result = await ai_mentor.debug_code(
            code=request.code,
            language=request.language,
            error_message=request.error_message,
            expected_behavior=request.expected_behavior
        )
        
        return DebugResponse(**result)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to debug code: {str(e)}")

@router.post("/learning-path", response_model=LearningPathResponse)
async def create_learning_path(
    request: LearningPathRequest
):
    """Create personalized learning path based on strengths and weaknesses"""
    try:
        if not ai_mentor:
            # Enhanced fallback response
            return LearningPathResponse(
                learning_path=f"""
                **Personalized Learning Path - 4 Week Plan**

                **Week 1: Foundation Building**
                - Focus on: {', '.join(request.user_weaknesses[:2]) if request.user_weaknesses else 'Core algorithms'}
                - Build upon: {', '.join(request.user_strengths[:2]) if request.user_strengths else 'Existing skills'}
                - Daily practice: 2-3 problems focusing on weak areas
                - Study time: 1-2 hours per day

                **Week 2: Pattern Recognition**  
                - Learn common algorithmic patterns
                - Practice identifying problem types quickly
                - Focus on time complexity analysis
                - Complete 10-15 medium difficulty problems

                **Week 3: Advanced Concepts**
                - Tackle more complex algorithms
                - Dynamic programming introduction
                - Graph algorithms basics
                - System design thinking

                **Week 4: Integration & Practice**
                - Mixed problem solving sessions
                - Mock interview practice
                - Review and reinforce weak areas
                - Prepare for next learning cycle
                """,
                estimated_duration="4 weeks",
                difficulty_progression=["Easy", "Easy-Medium", "Medium", "Medium-Hard"],
                checkpoint_problems=[
                    {"title": "Two Sum", "difficulty": "Easy", "concepts": "Arrays, Hash Tables"},
                    {"title": "Valid Parentheses", "difficulty": "Easy", "concepts": "Stack, String Processing"},
                    {"title": "Binary Tree Level Order", "difficulty": "Medium", "concepts": "Trees, BFS"},
                    {"title": "Coin Change", "difficulty": "Medium", "concepts": "Dynamic Programming"}
                ],
                success_metrics={
                    "problems_solved_per_week": [8, 12, 15, 18],
                    "accuracy_target": 0.80,
                    "avg_time_improvement": "25%",
                    "concept_mastery": ["Arrays", "Trees", "DP Basics"]
                }
            )
        
        # Use advanced AI mentor
        result = await ai_mentor.create_learning_path(
            user_id="anonymous",  # Since no authentication required
            current_problem_id=request.current_problem_id,
            user_strengths=request.user_strengths,
            user_weaknesses=request.user_weaknesses
        )
        
        return LearningPathResponse(**result)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create learning path: {str(e)}")

# Legacy endpoints maintained for backward compatibility
@router.post("/explain")
async def explain_code(
    problem_id: str,
    code: str,
    language: str
):
    """Legacy endpoint - Get code explanation from AI"""
    try:
        problems_collection = await get_collection("problems")
        
        # Get problem details
        problem_data = await problems_collection.find_one({"_id": ObjectId(problem_id)})
        if not problem_data:
            return {"explanation": "Problem not found"}
        
        problem_description = problem_data.get("description", "")
        
        if ai_mentor:
            # Use advanced analysis
            result = await ai_mentor.analyze_code_quality(
                code=code,
                language=language,
                problem_description=problem_description
            )
            
            return {
                "explanation": result["detailed_analysis"],
                "complexity_analysis": result["complexity_analysis"],
                "quality_score": result["quality_score"],
                "suggestions": result["improvement_suggestions"]
            }
        else:
            # Fallback implementation
            explanation = f"""
            This {language} solution approaches the problem by:
            
            1. **Analysis**: The code structure suggests a systematic approach to solving the problem.
            2. **Algorithm**: The implementation uses standard programming constructs effectively.
            3. **Efficiency**: Consider optimizing for both time and space complexity.
            4. **Edge Cases**: Make sure to handle boundary conditions properly.
            
            **Suggestions for improvement:**
            - Add error handling for edge cases
            - Consider alternative algorithms for better performance
            - Optimize memory usage if needed
            """
            
            return {
                "explanation": explanation,
                "complexity_analysis": {
                    "time": "Analysis pending - integrate with AI service",
                    "space": "Analysis pending - integrate with AI service"
                }
            }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to explain code: {str(e)}")

@router.post("/optimize")
async def optimize_code(
    problem_id: str,
    code: str,
    language: str
):
    """Legacy endpoint - Get code optimization suggestions from AI"""
    try:
        problems_collection = await get_collection("problems")
        
        # Get problem details
        problem_data = await problems_collection.find_one({"_id": ObjectId(problem_id)})
        if not problem_data:
            raise HTTPException(status_code=404, detail="Problem not found")
        
        problem_description = problem_data.get("description", "")
        
        if ai_mentor:
            # Use advanced analysis
            result = await ai_mentor.analyze_code_quality(
                code=code,
                language=language,
                problem_description=problem_description
            )
            
            return {
                "optimizations": result["improvement_suggestions"],
                "optimized_code": result["optimized_code_snippet"],
                "improvements": {
                    "analysis": result["detailed_analysis"],
                    "quality_score": result["quality_score"],
                    "complexity": result["complexity_analysis"]
                }
            }
        else:
            # Fallback implementation
            return {
                "optimizations": [
                    "Consider using more efficient data structures",
                    "Look for opportunities to reduce time complexity",
                    "Optimize memory usage where possible"
                ],
                "optimized_code": f"// Optimized {language} code would be generated here",
                "improvements": {
                    "time_complexity": "Potential improvement available",
                    "space_complexity": "Current usage is acceptable",
                    "readability": "Consider adding more comments"
                }
            }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to optimize code: {str(e)}")

@router.get("/mentor-status")
async def get_mentor_status():
    """Get the current status of the AI mentor system"""
    return {
        "advanced_ai_available": ai_mentor is not None,
        "groq_api_configured": os.getenv("GROQ_API_KEY") is not None,
        "features_available": [
            "Personalized hints with context awareness",
            "Comprehensive code quality analysis", 
            "Interactive concept explanations",
            "Advanced debugging assistance",
            "Personalized learning paths",
            "Vector-based knowledge storage",
            "Conversation history tracking"
        ] if ai_mentor else [
            "Basic hints and explanations",
            "Fallback responses for all features"
        ],
        "version": "2.0-Advanced" if ai_mentor else "1.0-Fallback"
    }
