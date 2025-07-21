# MongoDB Setup Guide for CodeForge

Since MongoDB is not installed on your local machine, you have several options:

## Option 1: MongoDB Atlas (Cloud) - Recommended for Quick Start

1. **Go to MongoDB Atlas**: https://www.mongodb.com/cloud/atlas
2. **Create a free account** and create a new cluster
3. **Get connection string**:
   - Click "Connect" on your cluster
   - Choose "Connect your application"
   - Copy the connection string (looks like: `mongodb+srv://username:password@cluster.mongodb.net/`)
4. **Update your `.env` file**:
   ```env
   MONGODB_URL=mongodb+srv://your-username:your-password@your-cluster.mongodb.net/
   DATABASE_NAME=codeforge
   ```

## Option 2: Install MongoDB Locally

### Windows Installation:
1. **Download MongoDB Community Server**:
   - Go to: https://www.mongodb.com/try/download/community
   - Download the Windows MSI installer
   - Run the installer (choose "Complete" installation)
   - Make sure to install MongoDB as a Service

2. **Start MongoDB Service**:
   ```powershell
   net start MongoDB
   ```

3. **Verify installation**:
   ```powershell
   mongod --version
   ```

## Option 3: Docker (Easiest for Development)

1. **Install Docker Desktop** from https://www.docker.com/products/docker-desktop

2. **Run MongoDB with Docker**:
   ```bash
   docker run --name mongodb -d -p 27017:27017 mongo:6.0
   ```

3. **Or use our Docker Compose** (from Backend directory):
   ```bash
   docker-compose up -d mongo
   ```

## Option 4: Use our Complete Docker Setup

From the Backend directory:
```bash
# Start all services (API + MongoDB + MongoDB Admin)
docker-compose up -d

# Initialize the database
docker-compose exec api python init_db_standalone.py
```

## Quick Test

After setting up MongoDB, test the connection:
```bash
python -c "
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
async def test():
    client = AsyncIOMotorClient('mongodb://localhost:27017')
    try:
        await client.admin.command('ping')
        print('✅ MongoDB connection successful!')
    except Exception as e:
        print(f'❌ Connection failed: {e}')
    finally:
        client.close()
asyncio.run(test())
"
```

Choose the option that works best for you and then run `python init_db_standalone.py` to initialize the database!
