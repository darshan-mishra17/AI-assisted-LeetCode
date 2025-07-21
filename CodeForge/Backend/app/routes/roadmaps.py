from fastapi import APIRouter, Depends
from typing import List, Dict, Any
from ..models.models import User, Roadmap, RoadmapTopic
from ..auth.auth import get_current_active_user
from ..database import get_collection
from bson import ObjectId
from datetime import datetime, timedelta

router = APIRouter(prefix="/roadmaps", tags=["roadmaps"])

@router.get("/", response_model=List[Dict[str, Any]])
async def get_roadmaps():
    """Get all available roadmaps"""
    roadmaps_collection = await get_collection("roadmaps")
    
    cursor = roadmaps_collection.find({})
    roadmaps_data = await cursor.to_list(length=None)
    
    roadmaps = []
    for roadmap_data in roadmaps_data:
        roadmaps.append({
            "id": str(roadmap_data["_id"]),
            "title": roadmap_data["title"],
            "description": roadmap_data["description"],
            "difficulty_level": roadmap_data["difficulty_level"],
            "estimated_weeks": roadmap_data["estimated_weeks"],
            "topics_count": len(roadmap_data.get("topics", []))
        })
    
    return roadmaps

@router.get("/{roadmap_id}")
async def get_roadmap_details(
    roadmap_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """Get detailed roadmap information"""
    roadmaps_collection = await get_collection("roadmaps")
    problems_collection = await get_collection("problems")
    
    roadmap_data = await roadmaps_collection.find_one({"_id": ObjectId(roadmap_id)})
    if not roadmap_data:
        return {"error": "Roadmap not found"}
    
    roadmap = Roadmap(**roadmap_data)
    
    # Get user's progress for this roadmap
    user_progress = current_user.roadmap_progress.get(roadmap_id, 0)
    
    # Enrich topics with problem details and progress
    enriched_topics = []
    for i, topic in enumerate(roadmap.topics):
        # Get problem details
        problem_details = []
        for problem_id in topic.problems:
            problem_data = await problems_collection.find_one({"_id": ObjectId(problem_id)})
            if problem_data:
                is_solved = problem_id in current_user.solved_problems
                problem_details.append({
                    "id": problem_id,
                    "title": problem_data["title"],
                    "slug": problem_data["slug"],
                    "difficulty": problem_data["difficulty"],
                    "is_solved": is_solved
                })
        
        # Calculate topic completion
        solved_count = sum(1 for p in problem_details if p["is_solved"])
        completion_percentage = (solved_count / len(problem_details)) * 100 if problem_details else 0
        
        # Check if topic is unlocked (based on prerequisites)
        is_unlocked = True
        if topic.prerequisites:
            for prereq_id in topic.prerequisites:
                prereq_topic = next((t for j, t in enumerate(roadmap.topics) if j < i and t.id == prereq_id), None)
                if prereq_topic:
                    # Check if prerequisite is completed
                    prereq_problems = []
                    for prob_id in prereq_topic.problems:
                        if prob_id in current_user.solved_problems:
                            prereq_problems.append(True)
                        else:
                            prereq_problems.append(False)
                    
                    if not all(prereq_problems):
                        is_unlocked = False
                        break
        
        enriched_topics.append({
            "id": topic.id,
            "title": topic.title,
            "description": topic.description,
            "problems": problem_details,
            "prerequisites": topic.prerequisites,
            "completion_percentage": completion_percentage,
            "is_unlocked": is_unlocked,
            "is_completed": completion_percentage == 100
        })
    
    # Calculate overall roadmap progress
    total_problems = sum(len(topic.problems) for topic in roadmap.topics)
    solved_problems = sum(1 for topic in enriched_topics 
                         for problem in topic["problems"] if problem["is_solved"])
    overall_progress = (solved_problems / total_problems) * 100 if total_problems > 0 else 0
    
    return {
        "id": str(roadmap.id),
        "title": roadmap.title,
        "description": roadmap.description,
        "difficulty_level": roadmap.difficulty_level,
        "estimated_weeks": roadmap.estimated_weeks,
        "topics": enriched_topics,
        "progress": {
            "percentage": overall_progress,
            "problems_solved": solved_problems,
            "total_problems": total_problems,
            "current_level": user_progress
        },
        "created_at": roadmap.created_at
    }

@router.post("/{roadmap_id}/start")
async def start_roadmap(
    roadmap_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """Start following a roadmap"""
    roadmaps_collection = await get_collection("roadmaps")
    users_collection = await get_collection("users")
    
    # Check if roadmap exists
    roadmap_exists = await roadmaps_collection.find_one({"_id": ObjectId(roadmap_id)})
    if not roadmap_exists:
        return {"error": "Roadmap not found"}
    
    # Add roadmap to user's progress
    await users_collection.update_one(
        {"_id": ObjectId(current_user.id)},
        {
            "$set": {
                f"roadmap_progress.{roadmap_id}": 0,
                "updated_at": datetime.utcnow()
            }
        }
    )
    
    return {"message": "Roadmap started successfully"}

@router.get("/user/progress")
async def get_user_roadmap_progress(current_user: User = Depends(get_current_active_user)):
    """Get user's progress across all roadmaps"""
    roadmaps_collection = await get_collection("roadmaps")
    
    user_roadmaps = []
    for roadmap_id, level in current_user.roadmap_progress.items():
        roadmap_data = await roadmaps_collection.find_one({"_id": ObjectId(roadmap_id)})
        if roadmap_data:
            roadmap = Roadmap(**roadmap_data)
            
            # Calculate progress
            total_problems = sum(len(topic.problems) for topic in roadmap.topics)
            solved_problems = sum(1 for topic in roadmap.topics 
                                for problem_id in topic.problems 
                                if problem_id in current_user.solved_problems)
            
            progress_percentage = (solved_problems / total_problems) * 100 if total_problems > 0 else 0
            
            user_roadmaps.append({
                "id": roadmap_id,
                "title": roadmap.title,
                "difficulty_level": roadmap.difficulty_level,
                "current_level": level,
                "progress_percentage": progress_percentage,
                "problems_solved": solved_problems,
                "total_problems": total_problems
            })
    
    return {"roadmaps": user_roadmaps}
