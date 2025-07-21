from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from ..schemas.schemas import UserProfile, UserUpdate, LeaderboardResponse, LeaderboardEntry
from ..models.models import User
from ..auth.auth import get_current_active_user
from ..database import get_collection
from ..utils.helpers import update_user_streak
from datetime import datetime, timedelta
from bson import ObjectId

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/profile/{username}", response_model=UserProfile)
async def get_user_profile(username: str):
    """Get user profile by username"""
    users_collection = await get_collection("users")
    user_data = await users_collection.find_one({"username": username})
    
    if not user_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    user = User(**user_data)
    return UserProfile(
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        avatar_url=user.avatar_url,
        bio=user.bio,
        github_url=user.github_url,
        linkedin_url=user.linkedin_url,
        role=user.role,
        stats=user.stats,
        badges=user.badges,
        created_at=user.created_at
    )

@router.put("/profile", response_model=UserProfile)
async def update_profile(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_active_user)
):
    """Update current user's profile"""
    users_collection = await get_collection("users")
    
    update_data = user_update.dict(exclude_unset=True)
    if update_data:
        update_data["updated_at"] = datetime.utcnow()
        
        await users_collection.update_one(
            {"_id": ObjectId(current_user.id)},
            {"$set": update_data}
        )
        
        # Get updated user
        updated_user_data = await users_collection.find_one({"_id": ObjectId(current_user.id)})
        updated_user = User(**updated_user_data)
        
        return UserProfile(
            username=updated_user.username,
            email=updated_user.email,
            full_name=updated_user.full_name,
            avatar_url=updated_user.avatar_url,
            bio=updated_user.bio,
            github_url=updated_user.github_url,
            linkedin_url=updated_user.linkedin_url,
            role=updated_user.role,
            stats=updated_user.stats,
            badges=updated_user.badges,
            created_at=updated_user.created_at
        )
    
    # Return current profile if no updates
    return UserProfile(
        username=current_user.username,
        email=current_user.email,
        full_name=current_user.full_name,
        avatar_url=current_user.avatar_url,
        bio=current_user.bio,
        github_url=current_user.github_url,
        linkedin_url=current_user.linkedin_url,
        role=current_user.role,
        stats=current_user.stats,
        badges=current_user.badges,
        created_at=current_user.created_at
    )

@router.get("/leaderboard", response_model=LeaderboardResponse)
async def get_leaderboard(
    limit: int = 50,
    current_user: User = Depends(get_current_active_user)
):
    """Get leaderboard of top users"""
    users_collection = await get_collection("users")
    
    # Get top users sorted by XP
    pipeline = [
        {"$sort": {"stats.xp": -1}},
        {"$limit": limit},
        {
            "$project": {
                "username": 1,
                "avatar_url": 1,
                "stats.xp": 1,
                "stats.total_problems_solved": 1
            }
        }
    ]
    
    cursor = users_collection.aggregate(pipeline)
    users = await cursor.to_list(length=limit)
    
    entries = []
    for i, user_data in enumerate(users):
        entries.append(LeaderboardEntry(
            username=user_data["username"],
            avatar_url=user_data.get("avatar_url"),
            xp=user_data["stats"]["xp"],
            problems_solved=user_data["stats"]["total_problems_solved"],
            rank=i + 1
        ))
    
    # Get current user's rank
    user_rank = None
    if current_user:
        rank_pipeline = [
            {"$sort": {"stats.xp": -1}},
            {"$group": {
                "_id": None,
                "users": {"$push": "$_id"}
            }},
            {"$unwind": {
                "path": "$users",
                "includeArrayIndex": "rank"
            }},
            {"$match": {"users": ObjectId(current_user.id)}},
            {"$project": {"rank": {"$add": ["$rank", 1]}}}
        ]
        
        rank_cursor = users_collection.aggregate(rank_pipeline)
        rank_result = await rank_cursor.to_list(length=1)
        if rank_result:
            user_rank = rank_result[0]["rank"]
    
    return LeaderboardResponse(entries=entries, user_rank=user_rank)

@router.get("/stats/{username}")
async def get_user_stats(username: str):
    """Get detailed user statistics"""
    users_collection = await get_collection("users")
    submissions_collection = await get_collection("submissions")
    
    user_data = await users_collection.find_one({"username": username})
    if not user_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    user = User(**user_data)
    
    # Get submission statistics
    submission_stats = await submissions_collection.aggregate([
        {"$match": {"user_id": str(user.id)}},
        {
            "$group": {
                "_id": "$status",
                "count": {"$sum": 1}
            }
        }
    ]).to_list(length=None)
    
    submission_counts = {stat["_id"]: stat["count"] for stat in submission_stats}
    
    # Get recent activity (last 30 days)
    thirty_days_ago = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    thirty_days_ago = thirty_days_ago - timedelta(days=30)
    
    recent_submissions = await submissions_collection.count_documents({
        "user_id": str(user.id),
        "submitted_at": {"$gte": thirty_days_ago}
    })
    
    return {
        "username": user.username,
        "stats": user.stats,
        "submission_stats": submission_counts,
        "recent_activity": recent_submissions,
        "badges": user.badges,
        "solved_problems": len(user.solved_problems)
    }
