# Quick Setup Instructions for CodeForge Backend

## ⚡ Quick Start (Cloud MongoDB - Recommended)

Since you don't have MongoDB installed locally, the fastest way to get started is with MongoDB Atlas (free cloud database):

### 1. Set up MongoDB Atlas (5 minutes)
1. Go to https://www.mongodb.com/cloud/atlas
2. Sign up for a free account
3. Create a new project
4. Create a free cluster (M0 Sandbox)
5. Create a database user:
   - Go to "Database Access"
   - Click "Add New Database User"
   - Choose "Password" authentication
   - Username: `codeforge`, Password: `password123` (or your choice)
   - Give "Atlas Admin" permissions
6. Set up network access:
   - Go to "Network Access"
   - Click "Add IP Address"
   - Choose "Allow Access From Anywhere" (0.0.0.0/0) for development
7. Get connection string:
   - Go to "Database" → Click "Connect" on your cluster
   - Choose "Connect your application"
   - Copy the connection string

### 2. Update your .env file
Replace the MONGODB_URL in your `.env` file:
```env
# Replace with your actual connection string
MONGODB_URL=mongodb+srv://codeforge:password123@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
DATABASE_NAME=codeforge
```

### 3. Test and Initialize
```bash
# Test connection
python test_mongo.py

# If connection works, initialize database
python init_db_standalone.py

# Start the API server
cd app
python main.py
```

## 🐳 Alternative: Local MongoDB with Docker (if you have Docker)

If you have Docker installed:
```bash
# Start MongoDB container
docker run --name mongodb -d -p 27017:27017 mongo:6.0

# Keep MONGODB_URL as is in .env:
# MONGODB_URL=mongodb://localhost:27017

# Initialize database
python init_db_standalone.py
```

## 💻 Alternative: Install MongoDB Locally

1. Download from: https://www.mongodb.com/try/download/community
2. Install MongoDB Community Server
3. Start MongoDB service
4. Run initialization script

## ✅ What's Ready

Your FastAPI backend is complete with:
- ✅ Authentication (JWT)
- ✅ User management
- ✅ Problem CRUD
- ✅ Code submissions
- ✅ Discussion forum
- ✅ AI mentor endpoints
- ✅ Admin panel
- ✅ Leaderboard system

## 🚀 Once MongoDB is Connected

1. **Initialize database**: `python init_db_standalone.py`
2. **Start API server**: `cd app && python main.py`
3. **Visit docs**: http://localhost:8000/docs
4. **Test login**:
   - Admin: admin / admin123
   - User: johndev / password123

The MongoDB Atlas option is recommended as it's free, requires no local installation, and works immediately!
