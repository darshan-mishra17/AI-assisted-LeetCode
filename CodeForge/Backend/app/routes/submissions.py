from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from ..schemas.schemas import SubmissionCreate, SubmissionResult
from ..models.models import User, Problem, Submission, SubmissionStatus
from ..auth.auth import get_current_active_user
from ..database import get_collection
from ..utils.helpers import execute_code, get_language_id, calculate_xp, update_user_streak
from bson import ObjectId
from datetime import datetime

router = APIRouter(prefix="/submissions", tags=["submissions"])

@router.post("/", response_model=SubmissionResult)
async def submit_solution(
    submission: SubmissionCreate,
    current_user: User = Depends(get_current_active_user)
):
    """Submit solution for a problem"""
    problems_collection = await get_collection("problems")
    submissions_collection = await get_collection("submissions")
    users_collection = await get_collection("users")
    
    # Get problem details
    problem_data = await problems_collection.find_one({"_id": ObjectId(submission.problem_id)})
    if not problem_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Problem not found"
        )
    
    problem = Problem(**problem_data)
    
    # Execute code against test cases
    test_cases = [tc.dict() for tc in problem.test_cases]
    execution_result = await execute_code(
        submission.code, 
        submission.language, 
        test_cases
    )
    
    # Map execution result to submission status
    status_map = {
        "accepted": SubmissionStatus.ACCEPTED,
        "wrong_answer": SubmissionStatus.WRONG_ANSWER,
        "time_limit_exceeded": SubmissionStatus.TIME_LIMIT_EXCEEDED,
        "memory_limit_exceeded": SubmissionStatus.MEMORY_LIMIT_EXCEEDED,
        "runtime_error": SubmissionStatus.RUNTIME_ERROR,
        "compilation_error": SubmissionStatus.COMPILATION_ERROR
    }
    
    submission_status = status_map.get(execution_result["status"], SubmissionStatus.RUNTIME_ERROR)
    
    # Create submission record
    new_submission = Submission(
        user_id=str(current_user.id),
        problem_id=submission.problem_id,
        language=submission.language,
        code=submission.code,
        status=submission_status,
        runtime=execution_result.get("runtime"),
        memory=execution_result.get("memory"),
        test_cases_passed=execution_result.get("test_cases_passed", 0),
        total_test_cases=execution_result.get("total_test_cases", 0),
        error_message=execution_result.get("error_message")
    )
    
    # Insert submission
    result = await submissions_collection.insert_one(new_submission.dict(by_alias=True))
    
    # Update problem statistics
    await problems_collection.update_one(
        {"_id": ObjectId(submission.problem_id)},
        {
            "$inc": {
                "total_submissions": 1,
                "total_accepted": 1 if submission_status == SubmissionStatus.ACCEPTED else 0
            }
        }
    )
    
    # Update acceptance rate
    updated_problem = await problems_collection.find_one({"_id": ObjectId(submission.problem_id)})
    if updated_problem["total_submissions"] > 0:
        acceptance_rate = (updated_problem["total_accepted"] / updated_problem["total_submissions"]) * 100
        await problems_collection.update_one(
            {"_id": ObjectId(submission.problem_id)},
            {"$set": {"acceptance_rate": round(acceptance_rate, 2)}}
        )
    
    # If accepted, update user statistics
    if submission_status == SubmissionStatus.ACCEPTED:
        # Check if it's the first solve for this problem
        is_first_solve = submission.problem_id not in current_user.solved_problems
        
        if is_first_solve:
            # Calculate XP
            xp_gained = calculate_xp(problem.difficulty.value)
            
            # Update user streak
            current_streak, max_streak = update_user_streak(current_user.stats.last_active)
            
            update_query = {
                "$addToSet": {"solved_problems": submission.problem_id},
                "$inc": {
                    "stats.total_problems_solved": 1,
                    "stats.xp": xp_gained,
                    f"stats.{problem.difficulty.value}_solved": 1
                },
                "$set": {
                    "stats.last_active": datetime.utcnow(),
                    "updated_at": datetime.utcnow()
                }
            }
            
            # Update streak if needed
            if current_streak == "increment":
                update_query["$inc"]["stats.current_streak"] = 1
                # Check if it's a new max streak
                if current_user.stats.current_streak + 1 > current_user.stats.max_streak:
                    update_query["$set"]["stats.max_streak"] = current_user.stats.current_streak + 1
            elif current_streak == 1:
                update_query["$set"]["stats.current_streak"] = 1
                if 1 > current_user.stats.max_streak:
                    update_query["$set"]["stats.max_streak"] = 1
            
            await users_collection.update_one(
                {"_id": ObjectId(current_user.id)},
                update_query
            )
    
    return SubmissionResult(
        id=str(result.inserted_id),
        status=submission_status,
        runtime=new_submission.runtime,
        memory=new_submission.memory,
        test_cases_passed=new_submission.test_cases_passed,
        total_test_cases=new_submission.total_test_cases,
        error_message=new_submission.error_message,
        submitted_at=new_submission.submitted_at
    )

@router.get("/", response_model=List[SubmissionResult])
async def get_user_submissions(
    problem_id: str = None,
    limit: int = 50,
    current_user: User = Depends(get_current_active_user)
):
    """Get user's submissions"""
    submissions_collection = await get_collection("submissions")
    
    filter_query = {"user_id": str(current_user.id)}
    if problem_id:
        filter_query["problem_id"] = problem_id
    
    cursor = submissions_collection.find(filter_query).sort("submitted_at", -1).limit(limit)
    submissions_data = await cursor.to_list(length=limit)
    
    submissions = []
    for sub_data in submissions_data:
        submission = Submission(**sub_data)
        submissions.append(SubmissionResult(
            id=str(submission.id),
            status=submission.status,
            runtime=submission.runtime,
            memory=submission.memory,
            test_cases_passed=submission.test_cases_passed,
            total_test_cases=submission.total_test_cases,
            error_message=submission.error_message,
            submitted_at=submission.submitted_at
        ))
    
    return submissions

@router.get("/{submission_id}", response_model=dict)
async def get_submission_details(
    submission_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """Get detailed submission information"""
    submissions_collection = await get_collection("submissions")
    
    submission_data = await submissions_collection.find_one({"_id": ObjectId(submission_id)})
    if not submission_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Submission not found"
        )
    
    submission = Submission(**submission_data)
    
    # Check if user owns this submission or is admin
    if submission.user_id != str(current_user.id) and current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    # Get problem details
    problems_collection = await get_collection("problems")
    problem_data = await problems_collection.find_one({"_id": ObjectId(submission.problem_id)})
    problem_title = problem_data["title"] if problem_data else "Unknown"
    
    return {
        "id": str(submission.id),
        "problem_id": submission.problem_id,
        "problem_title": problem_title,
        "language": submission.language,
        "code": submission.code,
        "status": submission.status,
        "runtime": submission.runtime,
        "memory": submission.memory,
        "test_cases_passed": submission.test_cases_passed,
        "total_test_cases": submission.total_test_cases,
        "error_message": submission.error_message,
        "submitted_at": submission.submitted_at
    }
