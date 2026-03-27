#!/bin/bash

# 1. Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Error: Docker is not installed. Please install it first."
    exit 1
fi

# 2. Start the containers
echo "🚀 Starting Scribe containers..."
docker compose up --build

# 3. Wait for Ollama API to be ready
echo "⏳ Waiting for Ollama engine to wake up..."
until curl -s http://localhost:11434/api/tags > /dev/null; do
  sleep 2
  echo "   ...still waiting..."
done

# 4. Pull the AI Models
echo "🧠 Downloading AI models (this may take a few minutes)..."
docker exec -it ollama ollama pull qwen2.5:7b

echo "------------------------------------------------"
echo "✅ SETUP COMPLETE!"
echo "📡 API: http://localhost:8000"
echo "📂 Outputs will appear in: ./outputs"
echo "------------------------------------------------"