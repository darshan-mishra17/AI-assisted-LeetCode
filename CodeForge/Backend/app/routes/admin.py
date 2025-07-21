from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Dict, Any
from ..schemas.schemas import ProblemCreate, ProblemUpdate, UserProfile
from ..models.models import User, Problem, Roadmap, RoadmapTopic
from ..auth.auth import get_admin_user
from ..database import get_collection
from bson import ObjectId
from datetime import datetime, timedelta

router = APIRouter(prefix="/admin", tags=["admin"])

@router.get("/stats")
async def get_admin_stats(admin_user: User = Depends(get_admin_user)):
    """Get platform statistics for admin dashboard"""
    users_collection = await get_collection("users")
    problems_collection = await get_collection("problems")
    submissions_collection = await get_collection("submissions")
    discussions_collection = await get_collection("discussions")
    
    # Get basic counts
    total_users = await users_collection.count_documents({})
    total_problems = await problems_collection.count_documents({})
    total_submissions = await submissions_collection.count_documents({})
    total_discussions = await discussions_collection.count_documents({})
    
    # Get active users (last 30 days)
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    active_users = await users_collection.count_documents({
        "stats.last_active": {"$gte": thirty_days_ago}
    })
    
    # Get submissions by status
    submission_stats = await submissions_collection.aggregate([
        {
            "$group": {
                "_id": "$status",
                "count": {"$sum": 1}
            }
        }
    ]).to_list(length=None)
    
    submission_by_status = {stat["_id"]: stat["count"] for stat in submission_stats}
    
    # Get problems by difficulty
    problem_stats = await problems_collection.aggregate([
        {
            "$group": {
                "_id": "$difficulty",
                "count": {"$sum": 1}
            }
        }
    ]).to_list(length=None)
    
    problems_by_difficulty = {stat["_id"]: stat["count"] for stat in problem_stats}
    
    # Get recent activity (last 7 days)
    seven_days_ago = datetime.utcnow() - timedelta(days=7)
    recent_submissions = await submissions_collection.count_documents({
        "submitted_at": {"$gte": seven_days_ago}
    })
    
    recent_signups = await users_collection.count_documents({
        "created_at": {"$gte": seven_days_ago}
    })
    
    return {
        "overview": {
            "total_users": total_users,
            "active_users": active_users,
            "total_problems": total_problems,
            "total_submissions": total_submissions,
            "total_discussions": total_discussions
        },
        "submissions": {
            "by_status": submission_by_status,
            "recent_count": recent_submissions
        },
        "problems": {
            "by_difficulty": problems_by_difficulty
        },
        "recent_activity": {
            "new_signups": recent_signups,
            "submissions": recent_submissions
        }
    }

@router.get("/users", response_model=List[Dict[str, Any]])
async def get_all_users(
    page: int = 1,
    limit: int = 50,
    search: str = None,
    admin_user: User = Depends(get_admin_user)
):
    """Get all users with pagination and search"""
    users_collection = await get_collection("users")
    
    # Build filter query
    filter_query = {}
    if search:
        filter_query["$or"] = [
            {"username": {"$regex": search, "$options": "i"}},
            {"email": {"$regex": search, "$options": "i"}},
            {"full_name": {"$regex": search, "$options": "i"}}
        ]
    
    # Get users with pagination
    skip = (page - 1) * limit
    cursor = users_collection.find(filter_query).skip(skip).limit(limit).sort("created_at", -1)
    users_data = await cursor.to_list(length=limit)
    
    # Get total count
    total = await users_collection.count_documents(filter_query)
    
    users = []
    for user_data in users_data:
        user = User(**user_data)
        users.append({
            "id": str(user.id),
            "username": user.username,
            "email": user.email,
            "full_name": user.full_name,
            "role": user.role,
            "is_active": user.is_active,
            "stats": user.stats,
            "created_at": user.created_at,
            "updated_at": user.updated_at
        })
    
    return {
        "users": users,
        "pagination": {
            "page": page,
            "limit": limit,
            "total": total,
            "pages": (total + limit - 1) // limit
        }
    }

@router.put("/users/{user_id}")
async def update_user(
    user_id: str,
    updates: Dict[str, Any],
    admin_user: User = Depends(get_admin_user)
):
    """Update user details (admin only)"""
    users_collection = await get_collection("users")
    
    # Check if user exists
    user_exists = await users_collection.find_one({"_id": ObjectId(user_id)})
    if not user_exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Update user
    updates["updated_at"] = datetime.utcnow()
    await users_collection.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": updates}
    )
    
    return {"message": "User updated successfully"}

@router.delete("/users/{user_id}")
async def delete_user(
    user_id: str,
    admin_user: User = Depends(get_admin_user)
):
    """Delete user (admin only)"""
    users_collection = await get_collection("users")
    submissions_collection = await get_collection("submissions")
    discussions_collection = await get_collection("discussions")
    comments_collection = await get_collection("comments")
    
    # Check if user exists
    user_exists = await users_collection.find_one({"_id": ObjectId(user_id)})
    if not user_exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Delete user and related data
    await users_collection.delete_one({"_id": ObjectId(user_id)})
    await submissions_collection.delete_many({"user_id": user_id})
    await discussions_collection.delete_many({"author_id": user_id})
    await comments_collection.delete_many({"author_id": user_id})
    
    return {"message": "User deleted successfully"}

@router.post("/roadmaps", status_code=status.HTTP_201_CREATED)
async def create_roadmap(
    roadmap_data: Dict[str, Any],
    admin_user: User = Depends(get_admin_user)
):
    """Create a new roadmap (admin only)"""
    roadmaps_collection = await get_collection("roadmaps")
    
    # Validate and create roadmap topics
    topics = []
    for topic_data in roadmap_data.get("topics", []):
        topic = RoadmapTopic(
            id=topic_data["id"],
            title=topic_data["title"],
            description=topic_data["description"],
            problems=topic_data["problems"],
            prerequisites=topic_data.get("prerequisites", [])
        )
        topics.append(topic)
    
    roadmap = Roadmap(
        title=roadmap_data["title"],
        description=roadmap_data["description"],
        topics=topics,
        difficulty_level=roadmap_data["difficulty_level"],
        estimated_weeks=roadmap_data["estimated_weeks"]
    )
    
    result = await roadmaps_collection.insert_one(roadmap.dict(by_alias=True))
    
    return {
        "id": str(result.inserted_id),
        "message": "Roadmap created successfully"
    }

@router.put("/roadmaps/{roadmap_id}")
async def update_roadmap(
    roadmap_id: str,
    updates: Dict[str, Any],
    admin_user: User = Depends(get_admin_user)
):
    """Update roadmap (admin only)"""
    roadmaps_collection = await get_collection("roadmaps")
    
    # Check if roadmap exists
    roadmap_exists = await roadmaps_collection.find_one({"_id": ObjectId(roadmap_id)})
    if not roadmap_exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Roadmap not found"
        )
    
    # Process topics if provided
    if "topics" in updates:
        topics = []
        for topic_data in updates["topics"]:
            topic = RoadmapTopic(
                id=topic_data["id"],
                title=topic_data["title"],
                description=topic_data["description"],
                problems=topic_data["problems"],
                prerequisites=topic_data.get("prerequisites", [])
            )
            topics.append(topic.dict())
        updates["topics"] = topics
    
    await roadmaps_collection.update_one(
        {"_id": ObjectId(roadmap_id)},
        {"$set": updates}
    )
    
    return {"message": "Roadmap updated successfully"}

@router.delete("/roadmaps/{roadmap_id}")
async def delete_roadmap(
    roadmap_id: str,
    admin_user: User = Depends(get_admin_user)
):
    """Delete roadmap (admin only)"""
    roadmaps_collection = await get_collection("roadmaps")
    users_collection = await get_collection("users")
    
    # Check if roadmap exists
    roadmap_exists = await roadmaps_collection.find_one({"_id": ObjectId(roadmap_id)})
    if not roadmap_exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Roadmap not found"
        )
    
    # Delete roadmap
    await roadmaps_collection.delete_one({"_id": ObjectId(roadmap_id)})
    
    # Remove roadmap from user progress
    await users_collection.update_many(
        {},
        {"$unset": {f"roadmap_progress.{roadmap_id}": ""}}
    )
    
    return {"message": "Roadmap deleted successfully"}

@router.get("/discussions/flagged")
async def get_flagged_discussions(admin_user: User = Depends(get_admin_user)):
    """Get flagged discussions for moderation"""
    # This is a stub - you would implement flagging system
    return {"flagged_discussions": []}

@router.post("/discussions/{discussion_id}/moderate")
async def moderate_discussion(
    discussion_id: str,
    action: str,  # "approve", "delete", "flag"
    admin_user: User = Depends(get_admin_user)
):
    """Moderate a discussion"""
    discussions_collection = await get_collection("discussions")
    
    if action == "delete":
        await discussions_collection.delete_one({"_id": ObjectId(discussion_id)})
        return {"message": "Discussion deleted"}
    elif action == "approve":
        await discussions_collection.update_one(
            {"_id": ObjectId(discussion_id)},
            {"$set": {"moderated": True, "approved": True}}
        )
        return {"message": "Discussion approved"}
    elif action == "flag":
        await discussions_collection.update_one(
            {"_id": ObjectId(discussion_id)},
            {"$set": {"flagged": True}}
        )
        return {"message": "Discussion flagged"}
    
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Invalid action"
    )
