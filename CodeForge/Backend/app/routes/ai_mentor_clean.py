from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from ..schemas.schemas import AIHintRequest, AIHintResponse
from ..services.simple_ai_mentor import SimpleAIMentor
import os

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

# Enhanced response models
class EnhancedAIHintResponse(BaseModel):
    hint: str
    confidence_score: float
    suggested_next_steps: List[str]
    follow_up_questions: List[str]
    learning_resources: List[Dict[str, str]]
    estimated_completion_time: str

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

@router.post("/hint", response_model=EnhancedAIHintResponse)
async def get_hint(request: AIHintRequest):
    """Get AI-powered personalized hints for coding problems"""
    try:
        if not ai_mentor:
            # Fallback response when AI service is not available
            return EnhancedAIHintResponse(
                hint=f"For this {request.language} problem, consider breaking it down into smaller components. Look at the data structures you're using and think about whether there's a more efficient approach.",
                confidence_score=0.7,
                suggested_next_steps=[
                    "Identify the main algorithm pattern",
                    "Choose appropriate data structures",
                    "Consider edge cases"
                ],
                follow_up_questions=[
                    "What's your current approach?",
                    "Have you considered the time complexity?"
                ],
                learning_resources=[
                    {"title": "Algorithm Patterns", "url": "https://leetcode.com/explore/"}
                ],
                estimated_completion_time="15-30 minutes"
            )
        
        # Use the actual AI service
        result = await ai_mentor.get_personalized_hint(
            problem_title="Coding Problem",
            problem_description="Problem requiring algorithmic solution",
            user_code=request.user_code,
            user_level="intermediate"
        )
        
        return EnhancedAIHintResponse(
            hint=result.get("hint", "Unable to generate hint"),
            confidence_score=float(result.get("confidence", 0.8)),
            suggested_next_steps=[
                "Review the approach",
                "Think about edge cases",
                "Consider optimization"
            ],
            follow_up_questions=[
                "What's your current approach?",
                "Have you tested edge cases?"
            ],
            learning_resources=[
                {"title": "Algorithm Guide", "url": "https://leetcode.com/explore/"}
            ],
            estimated_completion_time="15-30 minutes"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate hint: {str(e)}")

@router.post("/analyze", response_model=CodeAnalysisResponse)
async def analyze_code(request: CodeAnalysisRequest):
    """Comprehensive code quality analysis with optimization suggestions"""
    try:
        if not ai_mentor:
            return CodeAnalysisResponse(
                detailed_analysis=f"**Code Analysis for {request.language}:**\n\nYour code structure looks good. Consider reviewing the algorithm efficiency and edge cases.",
                complexity_analysis={"time": "O(n)", "space": "O(1)"},
                quality_score=7.5,
                improvement_suggestions=["Add input validation", "Handle edge cases", "Optimize algorithm"],
                optimized_code_snippet="// Optimized version would go here"
            )
        
        result = await ai_mentor.analyze_user_code(
            code=request.code,
            problem_context=request.problem_description
        )
        
        return CodeAnalysisResponse(
            detailed_analysis=result.get("analysis", "Unable to analyze code"),
            complexity_analysis={"time": "Analysis pending", "space": "Analysis pending"},
            quality_score=8.0,
            improvement_suggestions=["Review the AI analysis above"],
            optimized_code_snippet="// Check the detailed analysis for optimization suggestions"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to analyze code: {str(e)}")

@router.post("/debug", response_model=DebugResponse)
async def debug_code(request: DebugRequest):
    """Advanced debugging assistance with step-by-step guidance"""
    try:
        if not ai_mentor:
            return DebugResponse(
                debug_analysis=f"**Debugging Analysis for {request.language} Code:**\n\nError: {request.error_message}\n\nPlease review your logic and check for common issues like off-by-one errors, null pointer exceptions, or incorrect data types.",
                suggested_fixes=["Check variable initialization", "Verify loop conditions", "Handle edge cases"],
                corrected_code="// Review the debug analysis and apply suggested fixes",
                prevention_tips=["Use debugging tools", "Add logging", "Test with edge cases"],
                testing_suggestions=[{"type": "Unit test", "description": "Test with sample inputs"}]
            )
        
        result = await ai_mentor.debug_code(
            code=request.code,
            error_message=request.error_message,
            expected_behavior=request.expected_behavior
        )
        
        return DebugResponse(
            debug_analysis=result.get("debug_suggestions", "Unable to debug code"),
            suggested_fixes=["Review the AI analysis above"],
            corrected_code="// Check the detailed analysis for corrected code",
            prevention_tips=["Use debugging best practices"],
            testing_suggestions=[{"type": "AI suggestion", "description": "Follow the debug analysis"}]
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to debug code: {str(e)}")

@router.post("/explain-concept", response_model=ConceptExplanationResponse)
async def explain_concept(request: ConceptExplanationRequest):
    """Get detailed explanation of programming concepts with examples"""
    try:
        if not ai_mentor:
            return ConceptExplanationResponse(
                explanation=f"**{request.concept.title()}** is a fundamental programming concept used in algorithm design.",
                related_concepts=["Data Structures", "Algorithms", "Complexity Analysis"],
                practice_problems=[{"title": "Practice Problem", "difficulty": "Medium"}],
                visual_aids="Concept visualization would be helpful here.",
                real_world_applications=["Software Engineering", "System Design"]
            )
        
        result = await ai_mentor.explain_concept(
            concept=request.concept,
            context=f"Explain for {request.user_level} level in {request.programming_language}"
        )
        
        return ConceptExplanationResponse(
            explanation=result.get("explanation", "Unable to explain concept"),
            related_concepts=["Algorithm Design", "Data Structures"],
            practice_problems=[{"title": "Related Problem", "difficulty": "Medium"}],
            visual_aids="Check the explanation for visual understanding",
            real_world_applications=["Software Development", "Problem Solving"]
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to explain concept: {str(e)}")

@router.post("/learning-path", response_model=LearningPathResponse)
async def create_learning_path(request: LearningPathRequest):
    """Create personalized learning path based on strengths and weaknesses"""
    try:
        if not ai_mentor:
            return LearningPathResponse(
                learning_path="**4-Week Learning Path:**\n\nWeek 1: Foundation building\nWeek 2: Core algorithms\nWeek 3: Advanced topics\nWeek 4: Practice and review",
                estimated_duration="4 weeks",
                difficulty_progression=["Easy", "Medium", "Hard"],
                checkpoint_problems=[{"title": "Milestone Problem", "week": "Week 1"}],
                success_metrics={"problems_solved": 20, "concepts_mastered": 5}
            )
        
        result = await ai_mentor.get_learning_path(
            current_skills=request.user_strengths,
            target_goal="Master algorithmic problem solving"
        )
        
        return LearningPathResponse(
            learning_path=result.get("learning_path", "Custom learning path created"),
            estimated_duration="4 weeks",
            difficulty_progression=["Easy", "Medium", "Hard"],
            checkpoint_problems=[{"title": "Progress Check", "week": "Weekly"}],
            success_metrics={"target": "Improved problem-solving skills"}
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create learning path: {str(e)}")

# Legacy endpoints for backward compatibility
@router.post("/explain")
async def explain_code(problem_id: str, code: str, language: str):
    """Legacy endpoint - Get code explanation from AI"""
    try:
        if not ai_mentor:
            return {"explanation": f"This {language} code appears to implement a solution for the given problem. Consider reviewing the algorithm efficiency and edge cases."}
        
        result = await ai_mentor.analyze_user_code(
            code=code,
            problem_context="Code explanation request"
        )
        
        return {"explanation": result.get("analysis", "Unable to explain code")}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to explain code: {str(e)}")

@router.post("/optimize")
async def optimize_code(problem_id: str, code: str, language: str):
    """Legacy endpoint - Get code optimization suggestions from AI"""
    try:
        if not ai_mentor:
            return {
                "suggestions": f"Consider optimizing your {language} code by reviewing the algorithm complexity and data structure choices.",
                "complexity_analysis": {
                    "current": "Analysis pending",
                    "optimized": "Analysis pending"
                }
            }
        
        result = await ai_mentor.analyze_user_code(
            code=code,
            problem_context="Code optimization request"
        )
        
        return {
            "suggestions": result.get("analysis", "Unable to optimize code"),
            "complexity_analysis": {
                "current": "Check AI analysis",
                "optimized": "Follow AI suggestions"
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to optimize code: {str(e)}")
