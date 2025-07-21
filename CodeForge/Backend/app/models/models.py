from pydantic import BaseModel, Field, EmailStr, ConfigDict
from pydantic_core import core_schema
from typing import List, Optional, Dict, Any, Annotated
from datetime import datetime
from enum import Enum
from bson import ObjectId

class PyObjectId(ObjectId):
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        return core_schema.json_or_python_schema(
            json_schema=core_schema.str_schema(),
            python_schema=core_schema.union_schema([
                core_schema.is_instance_schema(ObjectId),
                core_schema.chain_schema([
                    core_schema.str_schema(),
                    core_schema.no_info_plain_validator_function(cls.validate),
                ])
            ]),
            serialization=core_schema.plain_serializer_function_ser_schema(
                lambda x: str(x)
            ),
        )

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

class UserRole(str, Enum):
    USER = "user"
    ADMIN = "admin"

class ProblemDifficulty(str, Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"

class SubmissionStatus(str, Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    WRONG_ANSWER = "wrong_answer"
    TIME_LIMIT_EXCEEDED = "time_limit_exceeded"
    MEMORY_LIMIT_EXCEEDED = "memory_limit_exceeded"
    RUNTIME_ERROR = "runtime_error"
    COMPILATION_ERROR = "compilation_error"

class Badge(BaseModel):
    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True)
    
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str
    description: str
    icon: str
    criteria: Dict[str, Any]

class UserStats(BaseModel):
    total_problems_solved: int = 0
    easy_solved: int = 0
    medium_solved: int = 0
    hard_solved: int = 0
    xp: int = 0
    current_streak: int = 0
    max_streak: int = 0
    last_active: Optional[datetime] = None

class User(BaseModel):
    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True)
    
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    username: str = Field(..., min_length=3, max_length=30)
    email: EmailStr
    full_name: Optional[str] = None
    hashed_password: str
    role: UserRole = UserRole.USER
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Profile Information
    avatar_url: Optional[str] = None
    bio: Optional[str] = None
    github_url: Optional[str] = None
    linkedin_url: Optional[str] = None
    
    # Gaming/Progress
    stats: UserStats = Field(default_factory=UserStats)
    badges: List[str] = []  # Badge IDs
    solved_problems: List[str] = []  # Problem IDs
    roadmap_progress: Dict[str, int] = {}  # roadmap_id -> level

class TestCase(BaseModel):
    input: str
    expected_output: str
    is_sample: bool = False
    explanation: Optional[str] = None

class Problem(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    title: str
    slug: str = Field(..., pattern=r'^[a-z0-9-]+$')
    description: str
    difficulty: ProblemDifficulty
    topics: List[str] = []
    companies: List[str] = []
    
    # Code templates for different languages
    code_templates: Dict[str, str] = {}
    
    # Test cases
    test_cases: List[TestCase] = []
    
    # Constraints and hints
    constraints: List[str] = []
    hints: List[str] = []
    
    # Metadata
    created_by: str  # User ID
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Stats
    acceptance_rate: float = 0.0
    total_submissions: int = 0
    total_accepted: int = 0
    
    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True)

class Submission(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    user_id: str
    problem_id: str
    language: str
    code: str
    status: SubmissionStatus
    
    # Execution results
    runtime: Optional[float] = None  # in milliseconds
    memory: Optional[float] = None   # in MB
    test_cases_passed: int = 0
    total_test_cases: int = 0
    error_message: Optional[str] = None
    
    submitted_at: datetime = Field(default_factory=datetime.utcnow)
    
    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True)

class Discussion(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    title: str
    content: str
    author_id: str
    problem_id: Optional[str] = None  # If discussion is about a specific problem
    
    # Engagement
    upvotes: int = 0
    downvotes: int = 0
    upvoted_by: List[str] = []
    downvoted_by: List[str] = []
    
    # Comments
    comments_count: int = 0
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True)

class Comment(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    discussion_id: str
    author_id: str
    content: str
    parent_comment_id: Optional[str] = None  # For nested comments
    
    # Engagement
    upvotes: int = 0
    upvoted_by: List[str] = []
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True)

class RoadmapTopic(BaseModel):
    id: str
    title: str
    description: str
    problems: List[str]  # Problem IDs
    prerequisites: List[str] = []  # Topic IDs that must be completed first

class Roadmap(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    title: str
    description: str
    topics: List[RoadmapTopic] = []
    difficulty_level: str  # beginner, intermediate, advanced
    estimated_weeks: int
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True)
