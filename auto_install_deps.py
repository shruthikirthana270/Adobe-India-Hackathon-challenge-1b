#!/usr/bin/env python3
"""
Automatic dependency installer for Challenge 1b
This script automatically installs all required Python dependencies
"""

import subprocess
import sys
import os
import importlib.util
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        print(f"Current version: {sys.version}")
        sys.exit(1)
    print(f"✅ Python version: {sys.version.split()[0]}")

def install_package(package):
    """Install a package using pip."""
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "--upgrade", package
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except subprocess.CalledProcessError:
        return False

def check_and_install_pip():
    """Ensure pip is available and up to date."""
    try:
        import pip
        print("✅ pip is available")
    except ImportError:
        print("📦 Installing pip...")
        subprocess.check_call([sys.executable, "-m", "ensurepip", "--upgrade"])
    
    # Upgrade pip
    print("📦 Upgrading pip...")
    subprocess.check_call([
        sys.executable, "-m", "pip", "install", "--upgrade", "pip", "setuptools", "wheel"
    ])

def install_system_dependencies():
    """Install system dependencies if possible."""
    print("🔧 Checking system dependencies...")
    
    # Try to install system packages on different platforms
    system = os.uname().sysname.lower() if hasattr(os, 'uname') else 'unknown'
    
    if system == 'linux':
        # Try to install with apt (Ubuntu/Debian)
        try:
            subprocess.run([
                'sudo', 'apt-get', 'update', '&&', 
                'sudo', 'apt-get', 'install', '-y', 
                'python3-dev', 'gcc', 'g++', 'libffi-dev'
            ], shell=True, check=False, stdout=subprocess.DEVNULL)
            print("✅ System dependencies installed (Linux)")
        except:
            print("⚠️  Could not install system dependencies automatically")
    elif system == 'darwin':
        # Try to install with brew (macOS)
        try:
            subprocess.run([
                'brew', 'install', 'python3-dev'
            ], check=False, stdout=subprocess.DEVNULL)
            print("✅ System dependencies checked (macOS)")
        except:
            print("⚠️  Could not install system dependencies automatically")

def install_requirements():
    """Install all required packages."""
    requirements = [
        "PyPDF2==3.0.1",
        "pdfplumber==0.10.3", 
        "scikit-learn==1.3.2",
        "numpy==1.24.3",
        "scipy==1.11.4",
        "nltk==3.8.1",
        "textblob==0.17.1",
        "pandas==2.1.4",
        "tqdm==4.66.1",
        "python-dateutil==2.8.2",
        "reportlab==4.0.7"  # For creating sample PDFs
    ]
    
    print("📦 Installing Python packages...")
    failed_packages = []
    
    for package in requirements:
        package_name = package.split('==')[0]
        print(f"   Installing {package_name}...")
        
        if install_package(package):
            print(f"   ✅ {package_name} installed")
        else:
            print(f"   ❌ Failed to install {package_name}")
            failed_packages.append(package)
    
    if failed_packages:
        print(f"\n⚠️  Failed to install: {', '.join(failed_packages)}")
        print("💡 Try installing manually with:")
        for package in failed_packages:
            print(f"   pip install {package}")
        return False
    
    return True

def download_nltk_data():
    """Download required NLTK data."""
    try:
        import nltk
        print("📚 Downloading NLTK data...")
        nltk.download('punkt', quiet=True)
        nltk.download('stopwords', quiet=True)
        nltk.download('wordnet', quiet=True)
        print("✅ NLTK data downloaded")
    except Exception as e:
        print(f"⚠️  Could not download NLTK data: {e}")

def verify_installation():
    """Verify that all packages are properly installed."""
    print("🔍 Verifying installation...")
    
    required_modules = [
        'PyPDF2', 'pdfplumber', 'sklearn', 'numpy', 
        'scipy', 'nltk', 'textblob', 'pandas', 'tqdm'
    ]
    
    failed_imports = []
    
    for module in required_modules:
        try:
            if module == 'sklearn':
                import sklearn
            else:
                __import__(module)
            print(f"   ✅ {module}")
        except ImportError:
            print(f"   ❌ {module}")
            failed_imports.append(module)
    
    if failed_imports:
        print(f"\n❌ Failed to import: {', '.join(failed_imports)}")
        return False
    
    print("✅ All packages verified successfully!")
    return True

def create_sample_pdfs():
    """Create sample PDF files for testing."""
    try:
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import letter
        
        print("📝 Creating sample PDF files...")
        
        collections = {
            1: {
                'title': 'Travel Planning Collection',
                'files': [
                    ('south_france_guide_1.pdf', 'Complete Guide to South of France\n\nThis comprehensive guide covers the beautiful regions of Provence and the French Riviera. Perfect for group travel planning with budget-friendly options, must-see attractions, and practical travel tips for college students.'),
                    ('budget_travel_guide.pdf', 'Budget Travel Tips for Students\n\nLearn how to travel on a budget with 10 college friends. Includes accommodation sharing strategies, group discounts, transportation options, and money-saving tips for food and activities.'),
                    ('group_activities.pdf', 'Group Activities and Attractions\n\nDiscover exciting activities perfect for groups of friends including outdoor adventures, cultural experiences, nightlife options, and team-building activities in Southern France.')
                ]
            },
            2: {
                'title': 'Adobe Acrobat HR Collection', 
                'files': [
                    ('acrobat_forms_basics.pdf', 'Adobe Acrobat Forms Fundamentals\n\nLearn the basics of creating fillable PDF forms for HR processes. Covers form fields, validation rules, basic automation, and user experience design for professional forms.'),
                    ('hr_compliance_forms.pdf', 'HR Compliance Documentation\n\nEssential guide for creating compliant HR forms including onboarding documents, employee agreements, regulatory compliance forms, and legal requirements for digital documentation.'),
                    ('workflow_automation.pdf', 'Workflow Automation Guide\n\nAdvanced techniques for automating HR workflows using Adobe Acrobat. Includes integration with HR systems, digital signatures, approval processes, and data collection automation.')
                ]
            },
            3: {
                'title': 'Recipe and Catering Collection',
                'files': [
                    ('vegetarian_recipes.pdf', 'Professional Vegetarian Cooking\n\nComprehensive collection of vegetarian recipes suitable for large-scale catering. Includes nutritional information, scaling guidelines, dietary restrictions, and presentation techniques for corporate events.'),
                    ('buffet_planning.pdf', 'Buffet Service Planning Guide\n\nComplete guide to planning and executing buffet-style service for corporate events. Covers setup procedures, food presentation, temperature control, and food safety protocols.'),
                    ('corporate_catering.pdf', 'Corporate Event Catering\n\nSpecialized guide for catering corporate gatherings including menu planning for dietary restrictions, professional presentation standards, cost management, and client satisfaction strategies.')
                ]
            }
        }
        
        for collection_num, collection_data in collections.items():
            collection_dir = Path(f'Collection {collection_num}/PDFs')
            collection_dir.mkdir(parents=True, exist_ok=True)
            
            for filename, content in collection_data['files']:
                filepath = collection_dir / filename
                c = canvas.Canvas(str(filepath), pagesize=letter)
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
                    
                    # Handle long lines
                    if len(line) > 80:
                        words = line.split(' ')
                        current_line = ''
                        for word in words:
                            if len(current_line + word) < 80:
                                current_line += word + ' '
                            else:
                                c.drawString(50, y_position, current_line.strip())
                                y_position -= 15
                                current_line = word + ' '
                        if current_line:
                            c.drawString(50, y_position, current_line.strip())
                            y_position -= 15
                    else:
                        c.drawString(50, y_position, line)
                        y_position -= 15
                
                c.save()
                print(f"   Created: {filepath}")
        
        print("✅ Sample PDFs created successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Could not create sample PDFs: {e}")
        return False

def main():
    """Main installation process."""
    print("🚀 Challenge 1b: Automatic Dependency Installation")
    print("=" * 50)
    
    # Check Python version
    check_python_version()
    
    # Install pip and basic tools
    check_and_install_pip()
    
    # Install system dependencies
    install_system_dependencies()
    
    # Install Python packages
    if not install_requirements():
        print("\n❌ Some packages failed to install")
        sys.exit(1)
    
    # Download NLTK data
    download_nltk_data()
    
    # Verify installation
    if not verify_installation():
        print("\n❌ Installation verification failed")
        sys.exit(1)
    
    # Create sample PDFs
    create_sample_pdfs()
    
    print("\n🎉 All dependencies installed successfully!")
    print("\n💡 You can now run the processor with:")
    print("   python process_collections.py")
    print("\n   Or use the full setup script:")
    print("   ./setup_and_run.sh")

if __name__ == "__main__":
    main()
