from fastapi import APIRouter, Depends
from ..schemas.schemas import AIHintRequest, AIHintResponse
from ..models.models import User
from ..auth.auth import get_current_active_user
from ..database import get_collection
from ..utils.helpers import get_ai_hint
from bson import ObjectId

router = APIRouter(prefix="/ai", tags=["ai-mentor"])

@router.post("/hint", response_model=AIHintResponse)
async def get_hint(
    request: AIHintRequest,
    current_user: User = Depends(get_current_active_user)
):
    """Get AI-powered hint for a coding problem"""
    problems_collection = await get_collection("problems")
    
    # Get problem details
    problem_data = await problems_collection.find_one({"_id": ObjectId(request.problem_id)})
    if not problem_data:
        return AIHintResponse(
            hint="Problem not found",
            suggestions=[]
        )
    
    problem_description = problem_data["description"]
    
    # Get AI hint (stub implementation)
    hint = await get_ai_hint(
        problem_description,
        request.user_code,
        request.language,
        request.hint_type
    )
    
    # Generate suggestions based on hint type
    suggestions = []
    if request.hint_type == "explanation":
        suggestions = [
            "Try to understand the problem requirements first",
            "Consider the time and space complexity",
            "Think about edge cases"
        ]
    elif request.hint_type == "hint":
        suggestions = [
            "Look for patterns in the examples",
            "Consider using different data structures",
            "Break the problem into smaller parts"
        ]
    elif request.hint_type == "debug":
        suggestions = [
            "Check your variable names and types",
            "Verify your loop conditions",
            "Test with simple examples"
        ]
    
    return AIHintResponse(
        hint=hint,
        suggestions=suggestions
    )

@router.post("/explain")
async def explain_code(
    problem_id: str,
    code: str,
    language: str,
    current_user: User = Depends(get_current_active_user)
):
    """Get code explanation from AI"""
    problems_collection = await get_collection("problems")
    
    # Get problem details
    problem_data = await problems_collection.find_one({"_id": ObjectId(problem_id)})
    if not problem_data:
        return {"explanation": "Problem not found"}
    
    # Stub implementation for code explanation
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

@router.post("/optimize")
async def optimize_code(
    problem_id: str,
    code: str,
    language: str,
    current_user: User = Depends(get_current_active_user)
):
    """Get code optimization suggestions from AI"""
    # Stub implementation for code optimization
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
