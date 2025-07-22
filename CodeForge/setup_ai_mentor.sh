#!/bin/bash
# AI Mentor Setup Script - Initialize Advanced AI capabilities

echo "🤖 Setting up Advanced AI Mentor for CodeForge..."

# Navigate to backend directory
cd Backend

echo "📦 Installing Python AI dependencies..."

# Install the advanced AI mentor dependencies
pip install langchain>=0.1.0
pip install langchain-community>=0.0.10
pip install langchain-groq>=0.0.1
pip install chromadb>=0.4.0
pip install sentence-transformers>=2.2.0
pip install openai>=1.3.0
pip install tiktoken>=0.5.0
pip install numpy>=1.24.0
pip install pandas>=2.0.0

echo "✅ Python dependencies installed successfully!"

echo "🔧 Setting up vector database..."

# Create chroma database directory
mkdir -p chroma_db
touch chroma_db/.gitkeep

echo "✅ Vector database directory created!"

echo "📄 Setting up environment variables..."

# Check if .env file exists, if not create it
if [ ! -f .env ]; then
    echo "Creating .env file from template..."
    cp .env.example .env 2>/dev/null || echo "# CodeForge Backend Environment Variables" > .env
fi

# Add AI mentor variables if they don't exist
if ! grep -q "GROQ_API_KEY" .env; then
    echo "" >> .env
    echo "# AI Mentor Configuration" >> .env
    echo "GROQ_API_KEY=your_groq_api_key_here" >> .env
    echo "OPENAI_API_KEY=your_openai_api_key_here" >> .env
    echo "CHROMADB_PATH=./chroma_db" >> .env
    echo "AI_MENTOR_MODEL=mixtral-8x7b-32768" >> .env
    echo "AI_MENTOR_TEMPERATURE=0.1" >> .env
    echo "ENABLE_ADVANCED_AI=true" >> .env
fi

echo "✅ Environment variables configured!"

echo ""
echo "🎉 AI Mentor setup complete!"
echo ""
echo "📋 Next Steps:"
echo "1. Get your Groq API key from: https://console.groq.com/"
echo "2. Update the GROQ_API_KEY in your .env file"
echo "3. Restart your backend server"
echo "4. Test the AI mentor in the problem detail pages"
echo ""
echo "🚀 The AI Mentor now supports:"
echo "   • Personalized hints with context awareness"  
echo "   • Comprehensive code quality analysis"
echo "   • Interactive concept explanations"
echo "   • Advanced debugging assistance"
echo "   • Personalized learning paths"
echo "   • Vector-based knowledge storage"
echo "   • Conversation history tracking"
echo ""
echo "💡 Pro tip: The AI mentor gets smarter as you use it more!"
