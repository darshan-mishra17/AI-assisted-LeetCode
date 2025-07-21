from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional
from ..schemas.schemas import (
    DiscussionCreate, DiscussionUpdate, DiscussionResponse,
    CommentCreate, CommentResponse
)
from ..models.models import Discussion, Comment, User
from ..auth.auth import get_current_active_user
from ..database import get_collection
from bson import ObjectId
from datetime import datetime

router = APIRouter(prefix="/discussions", tags=["discussions"])

@router.get("/", response_model=List[DiscussionResponse])
async def get_discussions(
    problem_id: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    sort_by: str = Query("recent", regex="^(recent|popular|oldest)$")
):
    """Get discussions with filtering and pagination"""
    discussions_collection = await get_collection("discussions")
    users_collection = await get_collection("users")
    problems_collection = await get_collection("problems")
    
    # Build filter query
    filter_query = {}
    if problem_id:
        filter_query["problem_id"] = problem_id
    
    # Sort options
    sort_options = {
        "recent": ("created_at", -1),
        "popular": ("upvotes", -1),
        "oldest": ("created_at", 1)
    }
    sort_field, sort_direction = sort_options[sort_by]
    
    # Get discussions with pagination
    skip = (page - 1) * limit
    cursor = discussions_collection.find(filter_query).sort(sort_field, sort_direction).skip(skip).limit(limit)
    discussions_data = await cursor.to_list(length=limit)
    
    discussions = []
    for discussion_data in discussions_data:
        discussion = Discussion(**discussion_data)
        
        # Get author username
        author_data = await users_collection.find_one({"_id": ObjectId(discussion.author_id)})
        author_username = author_data["username"] if author_data else "Unknown User"
        
        # Get problem title if discussion is about a specific problem
        problem_title = None
        if discussion.problem_id:
            problem_data = await problems_collection.find_one({"_id": ObjectId(discussion.problem_id)})
            problem_title = problem_data["title"] if problem_data else None
        
        discussions.append(DiscussionResponse(
            id=str(discussion.id),
            title=discussion.title,
            content=discussion.content,
            author_id=discussion.author_id,
            author_username=author_username,
            problem_id=discussion.problem_id,
            problem_title=problem_title,
            upvotes=discussion.upvotes,
            downvotes=discussion.downvotes,
            comments_count=discussion.comments_count,
            created_at=discussion.created_at,
            updated_at=discussion.updated_at
        ))
    
    return discussions

@router.post("/", response_model=DiscussionResponse, status_code=status.HTTP_201_CREATED)
async def create_discussion(
    discussion_data: DiscussionCreate,
    current_user: User = Depends(get_current_active_user)
):
    """Create a new discussion"""
    discussions_collection = await get_collection("discussions")
    problems_collection = await get_collection("problems")
    
    # Validate problem_id if provided
    if discussion_data.problem_id:
        problem_exists = await problems_collection.find_one({"_id": ObjectId(discussion_data.problem_id)})
        if not problem_exists:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Problem not found"
            )
    
    discussion = Discussion(
        title=discussion_data.title,
        content=discussion_data.content,
        author_id=str(current_user.id),
        problem_id=discussion_data.problem_id
    )
    
    result = await discussions_collection.insert_one(discussion.dict(by_alias=True))
    
    if result.inserted_id:
        # Get problem title if discussion is about a specific problem
        problem_title = None
        if discussion.problem_id:
            problem_data = await problems_collection.find_one({"_id": ObjectId(discussion.problem_id)})
            problem_title = problem_data["title"] if problem_data else None
        
        return DiscussionResponse(
            id=str(result.inserted_id),
            title=discussion.title,
            content=discussion.content,
            author_id=discussion.author_id,
            author_username=current_user.username,
            problem_id=discussion.problem_id,
            problem_title=problem_title,
            upvotes=discussion.upvotes,
            downvotes=discussion.downvotes,
            comments_count=discussion.comments_count,
            created_at=discussion.created_at,
            updated_at=discussion.updated_at
        )
    
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Failed to create discussion"
    )

@router.get("/{discussion_id}", response_model=DiscussionResponse)
async def get_discussion(discussion_id: str):
    """Get discussion details"""
    discussions_collection = await get_collection("discussions")
    users_collection = await get_collection("users")
    problems_collection = await get_collection("problems")
    
    discussion_data = await discussions_collection.find_one({"_id": ObjectId(discussion_id)})
    if not discussion_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Discussion not found"
        )
    
    discussion = Discussion(**discussion_data)
    
    # Get author username
    author_data = await users_collection.find_one({"_id": ObjectId(discussion.author_id)})
    author_username = author_data["username"] if author_data else "Unknown User"
    
    # Get problem title if discussion is about a specific problem
    problem_title = None
    if discussion.problem_id:
        problem_data = await problems_collection.find_one({"_id": ObjectId(discussion.problem_id)})
        problem_title = problem_data["title"] if problem_data else None
    
    return DiscussionResponse(
        id=str(discussion.id),
        title=discussion.title,
        content=discussion.content,
        author_id=discussion.author_id,
        author_username=author_username,
        problem_id=discussion.problem_id,
        problem_title=problem_title,
        upvotes=discussion.upvotes,
        downvotes=discussion.downvotes,
        comments_count=discussion.comments_count,
        created_at=discussion.created_at,
        updated_at=discussion.updated_at
    )

@router.put("/{discussion_id}", response_model=DiscussionResponse)
async def update_discussion(
    discussion_id: str,
    discussion_update: DiscussionUpdate,
    current_user: User = Depends(get_current_active_user)
):
    """Update a discussion (author only)"""
    discussions_collection = await get_collection("discussions")
    users_collection = await get_collection("users")
    problems_collection = await get_collection("problems")
    
    discussion_data = await discussions_collection.find_one({"_id": ObjectId(discussion_id)})
    if not discussion_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Discussion not found"
        )
    
    discussion = Discussion(**discussion_data)
    
    # Check if user is the author or admin
    if discussion.author_id != str(current_user.id) and current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this discussion"
        )
    
    update_data = discussion_update.dict(exclude_unset=True)
    if update_data:
        update_data["updated_at"] = datetime.utcnow()
        await discussions_collection.update_one(
            {"_id": ObjectId(discussion_id)},
            {"$set": update_data}
        )
    
    # Return updated discussion
    updated_discussion_data = await discussions_collection.find_one({"_id": ObjectId(discussion_id)})
    updated_discussion = Discussion(**updated_discussion_data)
    
    # Get problem title if discussion is about a specific problem
    problem_title = None
    if updated_discussion.problem_id:
        problem_data = await problems_collection.find_one({"_id": ObjectId(updated_discussion.problem_id)})
        problem_title = problem_data["title"] if problem_data else None
    
    return DiscussionResponse(
        id=str(updated_discussion.id),
        title=updated_discussion.title,
        content=updated_discussion.content,
        author_id=updated_discussion.author_id,
        author_username=current_user.username,
        problem_id=updated_discussion.problem_id,
        problem_title=problem_title,
        upvotes=updated_discussion.upvotes,
        downvotes=updated_discussion.downvotes,
        comments_count=updated_discussion.comments_count,
        created_at=updated_discussion.created_at,
        updated_at=updated_discussion.updated_at
    )

@router.delete("/{discussion_id}")
async def delete_discussion(
    discussion_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """Delete a discussion (author or admin only)"""
    discussions_collection = await get_collection("discussions")
    comments_collection = await get_collection("comments")
    
    discussion_data = await discussions_collection.find_one({"_id": ObjectId(discussion_id)})
    if not discussion_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Discussion not found"
        )
    
    discussion = Discussion(**discussion_data)
    
    # Check if user is the author or admin
    if discussion.author_id != str(current_user.id) and current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this discussion"
        )
    
    # Delete discussion and all its comments
    await discussions_collection.delete_one({"_id": ObjectId(discussion_id)})
    await comments_collection.delete_many({"discussion_id": discussion_id})
    
    return {"message": "Discussion deleted successfully"}

@router.post("/{discussion_id}/vote")
async def vote_discussion(
    discussion_id: str,
    vote_type: str,  # "upvote" or "downvote"
    current_user: User = Depends(get_current_active_user)
):
    """Vote on a discussion"""
    discussions_collection = await get_collection("discussions")
    
    if vote_type not in ["upvote", "downvote"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid vote type. Must be 'upvote' or 'downvote'"
        )
    
    discussion_data = await discussions_collection.find_one({"_id": ObjectId(discussion_id)})
    if not discussion_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Discussion not found"
        )
    
    user_id = str(current_user.id)
    
    # Remove user from both lists first
    await discussions_collection.update_one(
        {"_id": ObjectId(discussion_id)},
        {
            "$pull": {
                "upvoted_by": user_id,
                "downvoted_by": user_id
            }
        }
    )
    
    # Add user to appropriate list and update count
    if vote_type == "upvote":
        await discussions_collection.update_one(
            {"_id": ObjectId(discussion_id)},
            {
                "$addToSet": {"upvoted_by": user_id},
                "$inc": {"upvotes": 1}
            }
        )
    else:
        await discussions_collection.update_one(
            {"_id": ObjectId(discussion_id)},
            {
                "$addToSet": {"downvoted_by": user_id},
                "$inc": {"downvotes": 1}
            }
        )
    
    return {"message": f"Discussion {vote_type}d successfully"}

# Comments endpoints

@router.get("/{discussion_id}/comments", response_model=List[CommentResponse])
async def get_discussion_comments(
    discussion_id: str,
    page: int = Query(1, ge=1),
    limit: int = Query(50, ge=1, le=100)
):
    """Get comments for a discussion"""
    comments_collection = await get_collection("comments")
    users_collection = await get_collection("users")
    
    # Get comments with pagination
    skip = (page - 1) * limit
    cursor = comments_collection.find({"discussion_id": discussion_id}).sort("created_at", 1).skip(skip).limit(limit)
    comments_data = await cursor.to_list(length=limit)
    
    comments = []
    for comment_data in comments_data:
        comment = Comment(**comment_data)
        
        # Get author username
        author_data = await users_collection.find_one({"_id": ObjectId(comment.author_id)})
        author_username = author_data["username"] if author_data else "Unknown User"
        
        comments.append(CommentResponse(
            id=str(comment.id),
            discussion_id=comment.discussion_id,
            author_id=comment.author_id,
            author_username=author_username,
            content=comment.content,
            parent_comment_id=comment.parent_comment_id,
            upvotes=comment.upvotes,
            created_at=comment.created_at,
            updated_at=comment.updated_at
        ))
    
    return comments

@router.post("/{discussion_id}/comments", response_model=CommentResponse, status_code=status.HTTP_201_CREATED)
async def create_comment(
    discussion_id: str,
    comment_data: CommentCreate,
    current_user: User = Depends(get_current_active_user)
):
    """Create a comment on a discussion"""
    discussions_collection = await get_collection("discussions")
    comments_collection = await get_collection("comments")
    
    # Check if discussion exists
    discussion_exists = await discussions_collection.find_one({"_id": ObjectId(discussion_id)})
    if not discussion_exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Discussion not found"
        )
    
    comment = Comment(
        discussion_id=discussion_id,
        author_id=str(current_user.id),
        content=comment_data.content,
        parent_comment_id=comment_data.parent_comment_id
    )
    
    result = await comments_collection.insert_one(comment.dict(by_alias=True))
    
    if result.inserted_id:
        # Update discussion comment count
        await discussions_collection.update_one(
            {"_id": ObjectId(discussion_id)},
            {"$inc": {"comments_count": 1}}
        )
        
        return CommentResponse(
            id=str(result.inserted_id),
            discussion_id=comment.discussion_id,
            author_id=comment.author_id,
            author_username=current_user.username,
            content=comment.content,
            parent_comment_id=comment.parent_comment_id,
            upvotes=comment.upvotes,
            created_at=comment.created_at,
            updated_at=comment.updated_at
        )
    
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Failed to create comment"
    )
