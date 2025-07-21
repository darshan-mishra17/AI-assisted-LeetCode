from fastapi import APIRouter, Depends, HTTPException, status
from datetime import timedelta
from ..schemas.schemas import UserSignup, UserLogin, Token, UserProfile
from ..models.models import User, UserStats
from ..auth.auth import (
    authenticate_user, 
    create_access_token, 
    get_password_hash, 
    get_current_active_user,
    ACCESS_TOKEN_EXPIRE_MINUTES
)
from ..database import get_collection
from ..utils.helpers import create_slug
from bson import ObjectId
import os

router = APIRouter(prefix="/auth", tags=["authentication"])

@router.post("/signup", response_model=UserProfile, status_code=status.HTTP_201_CREATED)
async def signup(user_data: UserSignup):
    """Register a new user"""
    users_collection = await get_collection("users")
    
    # Check if username or email already exists
    existing_user = await users_collection.find_one({
        "$or": [
            {"username": user_data.username},
            {"email": user_data.email}
        ]
    })
    
    if existing_user:
        if existing_user["username"] == user_data.username:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already registered"
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
    
    # Create new user
    hashed_password = get_password_hash(user_data.password)
    user = User(
        username=user_data.username,
        email=user_data.email,
        full_name=user_data.full_name,
        hashed_password=hashed_password,
        stats=UserStats()
    )
    
    # Insert user into database
    result = await users_collection.insert_one(user.dict(by_alias=True))
    
    if result.inserted_id:
        # Return user profile (without sensitive data)
        return UserProfile(
            username=user.username,
            email=user.email,
            full_name=user.full_name,
            role=user.role,
            stats=user.stats.dict(),
            badges=user.badges,
            created_at=user.created_at
        )
    
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Failed to create user"
    )

@router.post("/login", response_model=Token)
async def login(user_credentials: UserLogin):
    """Authenticate user and return access token"""
    user = await authenticate_user(user_credentials.username, user_credentials.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserProfile)
async def get_current_user_profile(current_user: User = Depends(get_current_active_user)):
    """Get current user's profile"""
    return UserProfile(
        username=current_user.username,
        email=current_user.email,
        full_name=current_user.full_name,
        avatar_url=current_user.avatar_url,
        bio=current_user.bio,
        github_url=current_user.github_url,
        linkedin_url=current_user.linkedin_url,
        role=current_user.role,
        stats=current_user.stats.dict(),
        badges=current_user.badges,
        created_at=current_user.created_at
    )
