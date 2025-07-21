from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional
from ..schemas.schemas import (
    ProblemCreate, ProblemUpdate, ProblemSummary, 
    ProblemDetail, ProblemFilter
)
from ..models.models import Problem, User, TestCase
from ..auth.auth import get_current_active_user, get_admin_user
from ..database import get_collection
from ..utils.helpers import create_slug, paginate_results
from bson import ObjectId
from datetime import datetime

router = APIRouter(prefix="/problems", tags=["problems"])

@router.get("/", response_model=dict)
async def get_problems(
    difficulty: Optional[List[str]] = Query(None),
    topics: Optional[List[str]] = Query(None),
    companies: Optional[List[str]] = Query(None),
    status: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_active_user)
):
    """Get problems with filtering and pagination"""
    problems_collection = await get_collection("problems")
    
    # Build filter query
    filter_query = {}
    
    if difficulty:
        filter_query["difficulty"] = {"$in": difficulty}
    
    if topics:
        filter_query["topics"] = {"$in": topics}
    
    if companies:
        filter_query["companies"] = {"$in": companies}
    
    if search:
        filter_query["$or"] = [
            {"title": {"$regex": search, "$options": "i"}},
            {"description": {"$regex": search, "$options": "i"}}
        ]
    
    # Get total count
    total = await problems_collection.count_documents(filter_query)
    
    # Get problems with pagination
    skip = (page - 1) * limit
    cursor = problems_collection.find(filter_query).skip(skip).limit(limit)
    problems_data = await cursor.to_list(length=limit)
    
    problems = []
    for problem_data in problems_data:
        problem = Problem(**problem_data)
        
        # Check if user has solved this problem
        user_status = "not_attempted"
        if str(problem.id) in current_user.solved_problems:
            user_status = "solved"
        else:
            # Check if user has attempted (has submissions)
            submissions_collection = await get_collection("submissions")
            has_submission = await submissions_collection.find_one({
                "user_id": str(current_user.id),
                "problem_id": str(problem.id)
            })
            if has_submission:
                user_status = "attempted"
        
        problems.append({
            "id": str(problem.id),
            "title": problem.title,
            "slug": problem.slug,
            "difficulty": problem.difficulty,
            "topics": problem.topics,
            "companies": problem.companies,
            "acceptance_rate": problem.acceptance_rate,
            "total_submissions": problem.total_submissions,
            "status": user_status
        })
    
    # Apply status filter after adding user status
    if status and status != "all":
        problems = [p for p in problems if p["status"] == status]
    
    return {
        "problems": problems,
        "pagination": {
            "page": page,
            "limit": limit,
            "total": total,
            "pages": (total + limit - 1) // limit
        }
    }

@router.get("/public", response_model=dict)
async def get_problems_public(
    difficulty: Optional[List[str]] = Query(None),
    topics: Optional[List[str]] = Query(None),
    companies: Optional[List[str]] = Query(None),
    search: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100)
):
    """Get problems publicly without authentication"""
    problems_collection = await get_collection("problems")
    
    # Build filter query
    filter_query = {}
    
    if difficulty:
        filter_query["difficulty"] = {"$in": difficulty}
    
    if topics:
        filter_query["topics"] = {"$in": topics}
    
    if companies:
        filter_query["companies"] = {"$in": companies}
    
    if search:
        filter_query["$or"] = [
            {"title": {"$regex": search, "$options": "i"}},
            {"description": {"$regex": search, "$options": "i"}}
        ]
    
    # Get total count
    total = await problems_collection.count_documents(filter_query)
    
    # Get problems with pagination
    skip = (page - 1) * limit
    cursor = problems_collection.find(filter_query).skip(skip).limit(limit)
    problems_data = await cursor.to_list(length=limit)
    
    problems = []
    for problem_data in problems_data:
        problem = Problem(**problem_data)
        
        problems.append({
            "id": str(problem.id),
            "_id": str(problem.id),
            "title": problem.title,
            "slug": problem.slug,
            "difficulty": problem.difficulty,
            "topics": problem.topics,
            "tags": problem.topics,  # Alias for frontend compatibility
            "companies": problem.companies,
            "acceptance_rate": problem.acceptance_rate,
            "total_submissions": problem.total_submissions,
            "status": "not_attempted",  # Default for public view
            "description": problem.description
        })
    
    return {
        "problems": problems,
        "pagination": {
            "page": page,
            "limit": limit,
            "total": total,
            "pages": (total + limit - 1) // limit
        }
    }

@router.get("/public/{problem_slug}", response_model=ProblemDetail)
async def get_problem_public(problem_slug: str):
    """Get problem details by slug (public access)"""
    problems_collection = await get_collection("problems")
    problem_data = await problems_collection.find_one({"slug": problem_slug})
    
    if not problem_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Problem not found"
        )
    
    problem = Problem(**problem_data)
    
    return ProblemDetail(
        id=str(problem.id),
        title=problem.title,
        slug=problem.slug,
        description=problem.description,
        difficulty=problem.difficulty,
        topics=problem.topics,
        companies=problem.companies,
        examples=getattr(problem, 'examples', []),  # Handle missing examples
        constraints=problem.constraints if problem.constraints else [],
        test_cases=[
            {
                "input": tc.input,
                "expected_output": tc.expected_output,
                "is_hidden": getattr(tc, 'is_hidden', False)  # Handle missing is_hidden field
            }
            for tc in problem.test_cases
        ] if problem.test_cases else [],
        acceptance_rate=problem.acceptance_rate,
        total_submissions=problem.total_submissions,
        editorial=getattr(problem, 'editorial', None),  # Handle missing editorial
        hints=problem.hints,
        created_at=problem.created_at,
        updated_at=problem.updated_at
    )

@router.get("/{problem_slug}", response_model=ProblemDetail)
async def get_problem(
    problem_slug: str,
    current_user: User = Depends(get_current_active_user)
):
    """Get problem details by slug"""
    problems_collection = await get_collection("problems")
    problem_data = await problems_collection.find_one({"slug": problem_slug})
    
    if not problem_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Problem not found"
        )
    
    problem = Problem(**problem_data)
    
    return ProblemDetail(
        id=str(problem.id),
        title=problem.title,
        slug=problem.slug,
        description=problem.description,
        difficulty=problem.difficulty,
        topics=problem.topics,
        companies=problem.companies,
        code_templates=problem.code_templates,
        constraints=problem.constraints,
        hints=problem.hints,
        acceptance_rate=problem.acceptance_rate,
        total_submissions=problem.total_submissions,
        created_at=problem.created_at
    )

@router.post("/", response_model=ProblemDetail, status_code=status.HTTP_201_CREATED)
async def create_problem(
    problem_data: ProblemCreate,
    admin_user: User = Depends(get_admin_user)
):
    """Create a new problem (admin only)"""
    problems_collection = await get_collection("problems")
    
    # Create slug from title
    slug = create_slug(problem_data.title)
    
    # Check if slug already exists
    existing_problem = await problems_collection.find_one({"slug": slug})
    if existing_problem:
        # Append number to make it unique
        counter = 1
        while existing_problem:
            new_slug = f"{slug}-{counter}"
            existing_problem = await problems_collection.find_one({"slug": new_slug})
            counter += 1
        slug = new_slug
    
    # Convert test cases to TestCase objects
    test_cases = []
    for tc in problem_data.test_cases:
        test_cases.append(TestCase(
            input=tc["input"],
            expected_output=tc["expected_output"],
            is_sample=tc.get("is_sample", False),
            explanation=tc.get("explanation")
        ))
    
    problem = Problem(
        title=problem_data.title,
        slug=slug,
        description=problem_data.description,
        difficulty=problem_data.difficulty,
        topics=problem_data.topics,
        companies=problem_data.companies,
        code_templates=problem_data.code_templates,
        test_cases=test_cases,
        constraints=problem_data.constraints,
        hints=problem_data.hints,
        created_by=str(admin_user.id)
    )
    
    result = await problems_collection.insert_one(problem.dict(by_alias=True))
    
    if result.inserted_id:
        return ProblemDetail(
            id=str(result.inserted_id),
            title=problem.title,
            slug=problem.slug,
            description=problem.description,
            difficulty=problem.difficulty,
            topics=problem.topics,
            companies=problem.companies,
            code_templates=problem.code_templates,
            constraints=problem.constraints,
            hints=problem.hints,
            acceptance_rate=problem.acceptance_rate,
            total_submissions=problem.total_submissions,
            created_at=problem.created_at
        )
    
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Failed to create problem"
    )

@router.put("/{problem_id}", response_model=ProblemDetail)
async def update_problem(
    problem_id: str,
    problem_update: ProblemUpdate,
    admin_user: User = Depends(get_admin_user)
):
    """Update a problem (admin only)"""
    problems_collection = await get_collection("problems")
    
    # Check if problem exists
    existing_problem = await problems_collection.find_one({"_id": ObjectId(problem_id)})
    if not existing_problem:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Problem not found"
        )
    
    update_data = problem_update.dict(exclude_unset=True)
    if update_data:
        # Update slug if title changed
        if "title" in update_data:
            update_data["slug"] = create_slug(update_data["title"])
        
        # Convert test cases if provided
        if "test_cases" in update_data:
            test_cases = []
            for tc in update_data["test_cases"]:
                test_cases.append(TestCase(
                    input=tc["input"],
                    expected_output=tc["expected_output"],
                    is_sample=tc.get("is_sample", False),
                    explanation=tc.get("explanation")
                ).dict())
            update_data["test_cases"] = test_cases
        
        update_data["updated_at"] = datetime.utcnow()
        
        await problems_collection.update_one(
            {"_id": ObjectId(problem_id)},
            {"$set": update_data}
        )
    
    # Return updated problem
    updated_problem_data = await problems_collection.find_one({"_id": ObjectId(problem_id)})
    updated_problem = Problem(**updated_problem_data)
    
    return ProblemDetail(
        id=str(updated_problem.id),
        title=updated_problem.title,
        slug=updated_problem.slug,
        description=updated_problem.description,
        difficulty=updated_problem.difficulty,
        topics=updated_problem.topics,
        companies=updated_problem.companies,
        code_templates=updated_problem.code_templates,
        constraints=updated_problem.constraints,
        hints=updated_problem.hints,
        acceptance_rate=updated_problem.acceptance_rate,
        total_submissions=updated_problem.total_submissions,
        created_at=updated_problem.created_at
    )

@router.delete("/{problem_id}")
async def delete_problem(
    problem_id: str,
    admin_user: User = Depends(get_admin_user)
):
    """Delete a problem (admin only)"""
    problems_collection = await get_collection("problems")
    
    result = await problems_collection.delete_one({"_id": ObjectId(problem_id)})
    
    if result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Problem not found"
        )
    
    return {"message": "Problem deleted successfully"}

@router.get("/topics/list")
async def get_topics():
    """Get all unique topics"""
    problems_collection = await get_collection("problems")
    topics = await problems_collection.distinct("topics")
    return {"topics": sorted(topics)}

@router.get("/companies/list")
async def get_companies():
    """Get all unique companies"""
    problems_collection = await get_collection("problems")
    companies = await problems_collection.distinct("companies")
    return {"companies": sorted(companies)}
