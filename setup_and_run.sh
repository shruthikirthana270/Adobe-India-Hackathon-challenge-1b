#!/bin/bash

# Comprehensive setup and run script for Challenge 1b
# This script automatically handles all dependencies and setup

set -e  # Exit on any error

echo "🚀 Challenge 1b: Multi-Collection PDF Analysis Setup"
echo "=================================================="

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to install Docker if not present
install_docker() {
    echo "🐳 Installing Docker..."
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux installation
        curl -fsSL https://get.docker.com -o get-docker.sh
        sudo sh get-docker.sh
        sudo usermod -aG docker $USER
        rm get-docker.sh
        echo "✅ Docker installed. Please log out and back in, then run this script again."
        exit 0
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS installation
        echo "Please install Docker Desktop from https://www.docker.com/products/docker-desktop"
        exit 1
    else
        echo "❌ Unsupported OS for automatic Docker installation"
        echo "Please install Docker manually from https://docs.docker.com/get-docker/"
        exit 1
    fi
}

# Function to check system requirements
check_requirements() {
    echo "🔍 Checking system requirements..."
    
    # Check Docker
    if ! command_exists docker; then
        echo "⚠️  Docker not found"
        read -p "Would you like to install Docker automatically? (y/n): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            install_docker
        else
            echo "❌ Docker is required. Please install it manually."
            exit 1
        fi
    else
        echo "✅ Docker found: $(docker --version)"
    fi
    
    # Check if Docker daemon is running
    if ! docker info >/dev/null 2>&1; then
        echo "❌ Docker daemon is not running. Please start Docker and try again."
        exit 1
    fi
    
    # Check available disk space (need at least 2GB)
    available_space=$(df . | tail -1 | awk '{print $4}')
    if [ "$available_space" -lt 2097152 ]; then  # 2GB in KB
        echo "⚠️  Low disk space. At least 2GB recommended."
    fi
    
    # Check available memory
    if command_exists free; then
        available_mem=$(free -m | awk 'NR==2{printf "%.0f", $7}')
        if [ "$available_mem" -lt 1024 ]; then
            echo "⚠️  Low available memory. At least 1GB recommended."
        fi
    fi
}

# Function to setup directory structure
setup_directories() {
    echo "📁 Setting up directory structure..."
    
    # Create collection directories
    for i in {1..3}; do
        mkdir -p "Collection $i/PDFs"
        echo "   Created Collection $i/PDFs"
    done
    
    # Create additional directories for outputs and logs
    mkdir -p logs temp_downloads
    echo "   Created logs and temp directories"
}

# Function to download sample PDFs if none exist
download_sample_pdfs() {
    echo "📄 Checking for PDF files..."
    
    total_pdfs=0
    for i in {1..3}; do
        pdf_count=$(find "Collection $i/PDFs" -name "*.pdf" 2>/dev/null | wc -l)
        total_pdfs=$((total_pdfs + pdf_count))
    done
    
    if [ $total_pdfs -eq 0 ]; then
        echo "⚠️  No PDF files found in collections"
        echo "📥 Would you like to create sample PDF files for testing?"
        read -p "Create sample PDFs? (y/n): " -n 1 -r
        echo
        
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            create_sample_pdfs
        else
            echo "ℹ️  You can add your own PDF files to the Collection X/PDFs directories"
        fi
    else
        echo "✅ Found $total_pdfs PDF files across all collections"
    fi
}

# Function to create sample PDFs for testing
create_sample_pdfs() {
    echo "📝 Creating sample PDF files..."
    
    # Check if Python is available for creating sample PDFs
    if command_exists python3; then
        python3 -c "
import sys
try:
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import letter
    import os
    
    # Sample content for each collection
    collections = {
        1: {
            'title': 'Travel Planning Collection',
            'files': [
                ('south_france_guide_1.pdf', 'Complete Guide to South of France\n\nThis guide covers the beautiful regions of Provence and the French Riviera. Perfect for group travel planning with budget-friendly options and must-see attractions.'),
                ('budget_travel_guide.pdf', 'Budget Travel Tips\n\nLearn how to travel on a budget with 10 college friends. Includes accommodation sharing, group discounts, and money-saving strategies.'),
                ('group_activities.pdf', 'Group Activities and Attractions\n\nDiscover exciting activities perfect for groups of friends including outdoor adventures, cultural experiences, and nightlife options.')
            ]
        },
        2: {
            'title': 'Adobe Acrobat HR Collection',
            'files': [
                ('acrobat_forms_basics.pdf', 'Adobe Acrobat Forms Fundamentals\n\nLearn the basics of creating fillable PDF forms for HR processes. Covers form fields, validation, and basic automation.'),
                ('hr_compliance_forms.pdf', 'HR Compliance Documentation\n\nEssential guide for creating compliant HR forms including onboarding documents, employee agreements, and regulatory compliance forms.'),
                ('workflow_automation.pdf', 'Workflow Automation Guide\n\nAdvanced techniques for automating HR workflows using Adobe Acrobat. Includes integration with HR systems and digital signatures.')
            ]
        },
        3: {
            'title': 'Recipe and Catering Collection',
            'files': [
                ('vegetarian_recipes.pdf', 'Professional Vegetarian Cooking\n\nComprehensive collection of vegetarian recipes suitable for large-scale catering. Includes nutritional information and scaling guidelines.'),
                ('buffet_planning.pdf', 'Buffet Service Planning\n\nComplete guide to planning and executing buffet-style service for corporate events. Covers setup, presentation, and food safety.'),
                ('corporate_catering.pdf', 'Corporate Event Catering\n\nSpecialized guide for catering corporate gatherings including dietary restrictions, professional presentation, and cost management.')
            ]
        }
    }
    
    for collection_num, collection_data in collections.items():
        collection_dir = f'Collection {collection_num}/PDFs'
        os.makedirs(collection_dir, exist_ok=True)
        
        for filename, content in collection_data['files']:
            filepath = os.path.join(collection_dir, filename)
            c = canvas.Canvas(filepath, pagesize=letter)
            width, height = letter
            
            # Title
            c.setFont('Helvetica-Bold', 16)
            c.drawString(50, height - 50, collection_data['title'])
            
            # Content
            c.setFont('Helvetica', 12)
            lines = content.split('\n')
            y_position = height - 100
            
            for line in lines:
                if y_position < 50:
                    c.showPage()
                    y_position = height - 50
                c.drawString(50, y_position, line)
                y_position -= 20
            
            c.save()
            print(f'Created: {filepath}')
    
    print('Sample PDFs created successfully!')
    
except ImportError:
    print('reportlab not available. Please add your own PDF files to test.')
    sys.exit(1)
" 2>/dev/null || echo "⚠️  Could not create sample PDFs. Please add your own PDF files."
    else
        echo "⚠️  Python not available for creating sample PDFs"
    fi
}

# Function to build Docker image with progress
build_docker_image() {
    echo "🔨 Building Docker image..."
    echo "This may take a few minutes to download and install dependencies..."
    
    # Build with progress and error handling
    if docker build --platform linux/amd64 -t challenge-1b-processor . --progress=plain; then
        echo "✅ Docker image built successfully"
        
        # Show image size
        image_size=$(docker images challenge-1b-processor --format "table {{.Size}}" | tail -n 1)
        echo "📦 Image size: $image_size"
    else
        echo "❌ Docker build failed"
        echo "💡 Try running with more verbose output:"
        echo "   docker build --platform linux/amd64 -t challenge-1b-processor . --no-cache --progress=plain"
        exit 1
    fi
}

# Function to run the processor
run_processor() {
    echo "🔄 Running multi-collection processor..."
    
    # Create logs directory if it doesn't exist
    mkdir -p logs
    
    start_time=$(date +%s)
    
    # Run with proper volume mounting and logging
    if docker run --rm \
        -v "$(pwd):/app" \
        -v "$(pwd)/logs:/app/logs" \
        --name challenge-1b-runner \
        challenge-1b-processor 2>&1 | tee logs/processing.log; then
        
        end_time=$(date +%s)
        execution_time=$((end_time - start_time))
        
        echo "✅ Processing completed successfully in ${execution_time} seconds"
        return 0
    else
        echo "❌ Processing failed. Check logs/processing.log for details"
        return 1
    fi
}

# Function to validate outputs
validate_outputs() {
    echo "🔍 Validating outputs..."
    
    if docker run --rm \
        -v "$(pwd):/app" \
        challenge-1b-processor \
        python validate_outputs.py; then
        echo "✅ All outputs validated successfully"
    else
        echo "⚠️  Some outputs failed validation"
    fi
}

# Function to show results summary
show_results() {
    echo "📊 Results Summary"
    echo "=================="
    
    for i in {1..3}; do
        output_file="Collection $i/challenge1b_output.json"
        if [ -f "$output_file" ]; then
            if command_exists jq; then
                persona=$(jq -r '.metadata.persona' "$output_file" 2>/dev/null || echo "Unknown")
                docs=$(jq -r '.metadata.total_documents_processed' "$output_file" 2>/dev/null || echo "0")
                sections=$(jq -r '.metadata.total_sections_analyzed' "$output_file" 2>/dev/null || echo "0")
                echo "📋 Collection $i ($persona):"
                echo "   Documents processed: $docs"
                echo "   Sections analyzed: $sections"
            else
                file_size=$(stat -f%z "$output_file" 2>/dev/null || stat -c%s "$output_file" 2>/dev/null || echo "unknown")
                echo "📋 Collection $i: Output generated (${file_size} bytes)"
            fi
        else
            echo "❌ Collection $i: No output file found"
        fi
    done
    
    echo ""
    echo "📁 Output files location:"
    echo "   Collection 1/challenge1b_output.json"
    echo "   Collection 2/challenge1b_output.json" 
    echo "   Collection 3/challenge1b_output.json"
    echo ""
    echo "📝 Processing logs: logs/processing.log"
}

# Function to cleanup
cleanup() {
    echo "🧹 Cleaning up temporary files..."
    rm -rf temp_downloads
    docker system prune -f >/dev/null 2>&1 || true
}

# Main execution flow
main() {
    echo "Starting Challenge 1b setup and execution..."
    echo ""
    
    # Trap cleanup on exit
    trap cleanup EXIT
    
    # Run setup steps
    check_requirements
    setup_directories
    download_sample_pdfs
    build_docker_image
    
    echo ""
    echo "🎯 Ready to process collections!"
    echo ""
    
    # Run processing
    if run_processor; then
        validate_outputs
        show_results
        
        echo ""
        echo "🎉 Challenge 1b completed successfully!"
        echo ""
        echo "💡 Next steps:"
        echo "   - Review the generated JSON outputs"
        echo "   - Add more PDF files to collections for additional testing"
        echo "   - Modify persona configurations in challenge1b_input.json files"
    else
        echo ""
        echo "❌ Processing failed. Please check the logs for details."
        exit 1
    fi
}

# Run main function
main "$@"
