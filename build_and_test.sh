#!/bin/bash

# Enhanced build and test script with automatic dependency handling

echo "🚀 Challenge 1b: Enhanced Multi-Collection PDF Processor"
echo "======================================================"

# Check if setup script exists and is executable
if [ -f "setup_and_run.sh" ]; then
    echo "🔧 Using comprehensive setup script..."
    chmod +x setup_and_run.sh
    ./setup_and_run.sh
    exit $?
fi

# Fallback to Docker-only approach
echo "🐳 Using Docker-only approach..."

# Check if Docker is available
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed"
    echo "💡 Please install Docker or run: python auto_install_deps.py"
    exit 1
fi

# Build Docker image with automatic dependency installation
echo "🔨 Building Docker image with automatic dependency installation..."
docker build --platform linux/amd64 -t challenge-1b-processor . --progress=plain

if [ $? -eq 0 ]; then
    echo "✅ Docker image built successfully"
else
    echo "❌ Docker build failed"
    echo "💡 Try the Python setup: python auto_install_deps.py"
    exit 1
fi

# Create directories and run processor
echo "📁 Setting up directories..."
for i in {1..3}; do
    mkdir -p "Collection $i/PDFs"
done

echo "🔄 Running processor..."
docker run --rm -v $(pwd):/app challenge-1b-processor

echo "🎉 Processing completed!"
