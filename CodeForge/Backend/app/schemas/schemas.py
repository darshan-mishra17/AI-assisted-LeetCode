from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from ..models.models import UserRole, ProblemDifficulty, SubmissionStatus, UserStats

# Auth Schemas
class UserSignup(BaseModel):
    username: str = Field(..., min_length=3, max_length=30)
    email: EmailStr
    password: str = Field(..., min_length=6)
    full_name: Optional[str] = None

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

# User Schemas
class UserProfile(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None
    avatar_url: Optional[str] = None
    bio: Optional[str] = None
    github_url: Optional[str] = None
    linkedin_url: Optional[str] = None
    role: UserRole
    stats: Dict[str, Any]  # Changed from UserStats to Dict
    badges: List[str] = []
    created_at: datetime

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    bio: Optional[str] = None
    avatar_url: Optional[str] = None
    github_url: Optional[str] = None
    linkedin_url: Optional[str] = None

# Problem Schemas
class ProblemCreate(BaseModel):
    title: str
    description: str
    difficulty: ProblemDifficulty
    topics: List[str] = []
    companies: List[str] = []
    code_templates: Dict[str, str] = {}
    test_cases: List[Dict[str, Any]] = []
    constraints: List[str] = []
    hints: List[str] = []

class ProblemUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    difficulty: Optional[ProblemDifficulty] = None
    topics: Optional[List[str]] = None
    companies: Optional[List[str]] = None
    code_templates: Optional[Dict[str, str]] = None
    test_cases: Optional[List[Dict[str, Any]]] = None
    constraints: Optional[List[str]] = None
    hints: Optional[List[str]] = None

class ProblemSummary(BaseModel):
    id: str
    title: str
    slug: str
    difficulty: ProblemDifficulty
    topics: List[str]
    companies: List[str]
    acceptance_rate: float
    total_submissions: int

class ProblemDetail(BaseModel):
    id: str
    title: str
    slug: str
    description: str
    difficulty: ProblemDifficulty
    topics: List[str]
    companies: List[str]
    examples: List[Dict[str, str]] = []  # Add examples field
    code_templates: Dict[str, str] = {}
    constraints: List[str] = []
    hints: List[str] = []
    test_cases: List[Dict[str, Any]] = []  # Add test_cases field
    acceptance_rate: float
    total_submissions: int
    editorial: Optional[str] = None  # Add editorial field
    created_at: datetime
    updated_at: Optional[datetime] = None  # Add updated_at field

# Submission Schemas
class SubmissionCreate(BaseModel):
    problem_id: str
    language: str
    code: str

class SubmissionResult(BaseModel):
    id: str
    status: SubmissionStatus
    runtime: Optional[float] = None
    memory: Optional[float] = None
    test_cases_passed: int
    total_test_cases: int
    error_message: Optional[str] = None
    submitted_at: datetime

# Discussion Schemas
class DiscussionCreate(BaseModel):
    title: str
    content: str
    problem_id: Optional[str] = None

class DiscussionUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None

class DiscussionResponse(BaseModel):
    id: str
    title: str
    content: str
    author_id: str
    author_username: str
    problem_id: Optional[str] = None
    problem_title: Optional[str] = None
    upvotes: int
    downvotes: int
    comments_count: int
    created_at: datetime
    updated_at: datetime

class CommentCreate(BaseModel):
    content: str
    parent_comment_id: Optional[str] = None

class CommentResponse(BaseModel):
    id: str
    discussion_id: str
    author_id: str
    author_username: str
    content: str
    parent_comment_id: Optional[str] = None
    upvotes: int
    created_at: datetime
    updated_at: datetime

# AI Mentor Schemas
class AIHintRequest(BaseModel):
    problem_id: str
    user_code: str
    language: str
    hint_type: str = "explanation"  # explanation, hint, debug

class AIHintResponse(BaseModel):
    hint: str
    suggestions: List[str] = []

# Leaderboard Schemas
class LeaderboardEntry(BaseModel):
    username: str
    avatar_url: Optional[str] = None
    xp: int
    problems_solved: int
    rank: int

class LeaderboardResponse(BaseModel):
    entries: List[LeaderboardEntry]
    user_rank: Optional[int] = None

# Filter Schemas
class ProblemFilter(BaseModel):
    difficulty: Optional[List[ProblemDifficulty]] = None
    topics: Optional[List[str]] = None
    companies: Optional[List[str]] = None
    status: Optional[str] = None  # solved, attempted, not_attempted
    search: Optional[str] = None
    page: int = 1
    limit: int = 20
