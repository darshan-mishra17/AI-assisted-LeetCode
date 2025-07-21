# CodeForge Backend

A comprehensive FastAPI backend for a LeetCode-style coding platform with MongoDB integration.

## Features

- 🔐 **Authentication**: JWT-based auth with role-based access control
- 🧑‍💻 **User Management**: Profiles, XP system, badges, streaks
- 🧩 **Problems**: CRUD operations, filtering, difficulty levels
- 💻 **Code Execution**: Submit and evaluate code solutions
- 🤖 **AI Mentor**: AI-powered hints and code explanations
- 🧠 **Roadmaps**: Learning paths with progress tracking
- 🧵 **Discussions**: Forum with comments and voting
- 🏆 **Leaderboard**: User rankings and statistics
- 🔒 **Admin Panel**: Platform management and moderation

## Tech Stack

- **FastAPI**: Modern Python web framework
- **MongoDB**: NoSQL database with Motor (async driver)
- **Pydantic**: Data validation and serialization
- **JWT**: Authentication and authorization
- **Passlib**: Password hashing
- **Python-dotenv**: Environment variable management

## Project Structure

```
Backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── database.py          # MongoDB connection
│   ├── auth/
│   │   ├── __init__.py
│   │   └── auth.py          # Authentication logic
│   ├── models/
│   │   ├── __init__.py
│   │   └── models.py        # Pydantic models
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py          # Authentication routes
│   │   ├── users.py         # User management
│   │   ├── problems.py      # Problem CRUD
│   │   ├── submissions.py   # Code submissions
│   │   ├── discussions.py   # Forum/discussions
│   │   ├── ai_mentor.py     # AI assistance
│   │   ├── roadmaps.py      # Learning paths
│   │   └── admin.py         # Admin operations
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── schemas.py       # Request/response schemas
│   └── utils/
│       ├── __init__.py
│       └── helpers.py       # Utility functions
├── .env                     # Environment variables
├── .gitignore
└── requirements.txt
```

## Setup Instructions

### 1. Prerequisites

- Python 3.8+
- MongoDB (local or MongoDB Atlas)
- Git

### 2. Clone and Setup

```bash
# Clone the repository
git clone <your-repo-url>
cd CodeForge/Backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Environment Configuration

Create a `.env` file in the Backend directory:

```env
# Database Configuration
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=codeforge

# JWT Configuration
SECRET_KEY=your-super-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Environment
ENVIRONMENT=development

# Code Execution Service (Judge0 or custom)
JUDGE0_API_URL=https://judge0-ce.p.rapidapi.com
JUDGE0_API_KEY=your-judge0-api-key

# AI Service (OpenAI, Anthropic, etc.)
AI_API_KEY=your-ai-api-key
AI_MODEL=gpt-3.5-turbo

# CORS Settings
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173
```

### 4. Database Setup

Make sure MongoDB is running locally or configure MongoDB Atlas connection in the `.env` file.

The application will automatically create the necessary collections when you start using the endpoints.

### 5. Run the Application

```bash
# From the Backend directory
cd app
python main.py

# Or using uvicorn directly
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- **API**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc

## API Endpoints

### Authentication
- `POST /auth/signup` - Register new user
- `POST /auth/login` - User login
- `GET /auth/me` - Get current user profile

### Users
- `GET /users/profile/{username}` - Get user profile
- `PUT /users/profile` - Update current user profile
- `GET /users/leaderboard` - Get user leaderboard
- `GET /users/stats/{username}` - Get user statistics

### Problems
- `GET /problems/` - Get problems with filtering
- `GET /problems/{slug}` - Get problem details
- `POST /problems/` - Create problem (admin only)
- `PUT /problems/{id}` - Update problem (admin only)
- `DELETE /problems/{id}` - Delete problem (admin only)

### Submissions
- `POST /submissions/` - Submit code solution
- `GET /submissions/` - Get user submissions
- `GET /submissions/{id}` - Get submission details

### Discussions
- `GET /discussions/` - Get discussions
- `POST /discussions/` - Create discussion
- `GET /discussions/{id}` - Get discussion details
- `PUT /discussions/{id}` - Update discussion
- `DELETE /discussions/{id}` - Delete discussion
- `POST /discussions/{id}/vote` - Vote on discussion

### AI Mentor
- `POST /ai/hint` - Get AI-powered hints
- `POST /ai/explain` - Get code explanation
- `POST /ai/optimize` - Get optimization suggestions

### Roadmaps
- `GET /roadmaps/` - Get all roadmaps
- `GET /roadmaps/{id}` - Get roadmap details
- `POST /roadmaps/{id}/start` - Start following roadmap

### Admin
- `GET /admin/stats` - Platform statistics
- `GET /admin/users` - Manage users
- `POST /admin/roadmaps` - Create roadmaps
- `POST /admin/discussions/{id}/moderate` - Moderate discussions

## Database Collections

The application uses the following MongoDB collections:

- **users**: User profiles, stats, and progress
- **problems**: Coding problems with test cases
- **submissions**: Code submissions and results
- **discussions**: Forum discussions
- **comments**: Discussion comments
- **roadmaps**: Learning roadmaps
- **badges**: Achievement badges (optional)

## Development

### Adding New Features

1. Create new Pydantic models in `app/models/models.py`
2. Add request/response schemas in `app/schemas/schemas.py`
3. Create route handlers in appropriate files in `app/routes/`
4. Add utility functions to `app/utils/helpers.py`
5. Update the main app in `app/main.py` to include new routes

### Code Execution Integration

The current implementation includes stubs for code execution. To integrate with actual code execution:

1. **Judge0 API**: Update the Judge0 configuration in `.env` and implement the API calls in `utils/helpers.py`
2. **Custom Docker**: Implement custom Docker-based execution
3. **Other Services**: Integrate with services like HackerEarth API, Sphere Engine, etc.

### AI Integration

Update the AI functions in `utils/helpers.py` to integrate with:
- OpenAI GPT models
- Anthropic Claude
- Google PaLM API
- Other AI services

## Testing

```bash
# Install testing dependencies
pip install pytest pytest-asyncio httpx

# Run tests
pytest
```

## Deployment

### Docker Deployment

Create a `Dockerfile`:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY app/ ./app/

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Environment Variables for Production

Make sure to set secure values for:
- `SECRET_KEY`
- `MONGODB_URL` (MongoDB Atlas connection string)
- `JUDGE0_API_KEY`
- `AI_API_KEY`
- `ALLOWED_ORIGINS`

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License.
