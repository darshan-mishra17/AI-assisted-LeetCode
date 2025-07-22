from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv

# Import database connection functions
from .database import connect_to_mongo, close_mongo_connection

# Import route modules
from .routes import (
    auth, users, problems, submissions, 
    discussions, ai_mentor, roadmaps, admin, test
)

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    try:
        await connect_to_mongo()
        print("✅ Connected to MongoDB successfully")
    except Exception as e:
        print(f"❌ Failed to connect to MongoDB: {e}")
        print("💡 Please check your MONGODB_URL in .env file")
        print("💡 See QUICKSTART.md for MongoDB setup instructions")
        # Don't exit - let the app start without DB for now
    
    yield
    
    # Shutdown
    try:
        await close_mongo_connection()
        print("Disconnected from MongoDB")
    except:
        pass

# Create FastAPI instance
app = FastAPI(
    title="CodeForge API",
    description="A LeetCode-style coding platform backend",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS - Development setup
# Force development CORS settings for localhost:5173
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173", 
        "http://127.0.0.1:5173",
        "http://localhost:3000",  # Alternative ports
        "http://127.0.0.1:3000"
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(problems.router)
app.include_router(submissions.router)
app.include_router(discussions.router)
app.include_router(ai_mentor.router)
app.include_router(roadmaps.router)
app.include_router(admin.router)
app.include_router(test.router)

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to CodeForge API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }

# CORS test endpoint
@app.get("/cors-test")
async def cors_test():
    """Simple endpoint to test CORS configuration"""
    return {"message": "CORS is working!", "timestamp": "2025-07-22", "status": "success"}

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        # Try to ping MongoDB
        from .database import database
        if database.client:
            await database.client.admin.command('ping')
            db_status = "connected"
        else:
            db_status = "not_connected"
    except Exception as e:
        db_status = f"error: {str(e)}"
    
    return {
        "status": "healthy",
        "service": "CodeForge API",
        "version": "1.0.0",
        "database": db_status
    }

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler"""
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
            "error": str(exc) if os.getenv("ENVIRONMENT") == "development" else "Something went wrong"
        }
    )

# 404 handler
@app.exception_handler(404)
async def not_found_handler(request, exc):
    """404 handler"""
    return JSONResponse(
        status_code=404,
        content={
            "detail": "Endpoint not found",
            "path": str(request.url.path)
        }
    )

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(
        "main:app", 
        host="0.0.0.0", 
        port=port, 
        reload=True if os.getenv("ENVIRONMENT") == "development" else False
    )
