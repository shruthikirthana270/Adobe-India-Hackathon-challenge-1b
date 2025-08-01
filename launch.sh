#!/bin/bash

# Universal launcher for Challenge 1b
# Automatically detects the best method to run the processor

echo "🚀 Challenge 1b: Universal Launcher"
echo "=================================="

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check available options and recommend the best approach
echo "🔍 Detecting available tools..."

HAS_DOCKER=false
HAS_PYTHON=false

if command_exists docker; then
    echo "✅ Docker detected"
    HAS_DOCKER=true
fi

if command_exists python3; then
    echo "✅ Python 3 detected"
    HAS_PYTHON=true
elif command_exists python; then
    echo "✅ Python detected"
    HAS_PYTHON=true
fi

echo ""

# Recommend best approach
if [ "$HAS_DOCKER" = true ]; then
    echo "🐳 Recommended: Docker approach (most reliable)"
    echo "   This will automatically handle all dependencies in an isolated environment"
    echo ""
    read -p "Use Docker approach? (y/n): " -n 1 -r
    echo ""
    
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "🔧 Using Docker setup..."
        chmod +x setup_and_run.sh
        ./setup_and_run.sh
        exit $?
    fi
fi

if [ "$HAS_PYTHON" = true ]; then
    echo "🐍 Alternative: Python local approach"
    echo "   This will install dependencies locally and run the processor"
    echo ""
    read -p "Use Python local approach? (y/n): " -n 1 -r
    echo ""
    
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "🔧 Using Python local setup..."
        python3 run_local.py 2>/dev/null || python run_local.py
        exit $?
    fi
fi

# Manual instructions
echo "📋 Manual Setup Instructions:"
echo ""
echo "Option 1 - Docker (Recommended):"
echo "  1. Install Docker from https://docker.com"
echo "  2. Run: ./setup_and_run.sh"
echo ""
echo "Option 2 - Python Local:"
echo "  1. Ensure Python 3.8+ is installed"
echo "  2. Run: python auto_install_deps.py"
echo "  3. Run: python process_collections.py"
echo ""
echo "Option 3 - Manual Dependencies:"
echo "  1. pip install PyPDF2 pdfplumber scikit-learn numpy scipy nltk textblob pandas tqdm"
echo "  2. python process_collections.py"
echo ""

exit 1
