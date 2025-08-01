#!/usr/bin/env python3
"""
Quick fix script to get Challenge 1b working immediately
"""

import json
import sys
from pathlib import Path

def create_minimal_setup():
    """Create minimal setup to get the processor working."""
    print("🔧 Quick Fix: Setting up Challenge 1b")
    print("=" * 40)
    
    # Create directories
    print("📁 Creating directories...")
    for i in range(1, 4):
        Path(f"Collection {i}/PDFs").mkdir(parents=True, exist_ok=True)
        print(f"   Created Collection {i}/PDFs")
    
    # Create minimal input files if they don't exist
    print("📝 Creating input configuration files...")
    
    input_configs = {
        1: {
            "challenge_info": {
                "challenge_id": "round_1b_002",
                "test_case_name": "travel_planning_south_france"
            },
            "documents": [
                {"filename": "travel_guide.pdf", "title": "Travel Guide"}
            ],
            "persona": {"role": "Travel Planner"},
            "job_to_be_done": {"task": "Plan a 4-day trip for 10 college friends to South of France"}
        },
        2: {
            "challenge_info": {
                "challenge_id": "round_1b_003", 
                "test_case_name": "adobe_acrobat_hr_forms"
            },
            "documents": [
                {"filename": "forms_guide.pdf", "title": "Forms Guide"}
            ],
            "persona": {"role": "HR Professional"},
            "job_to_be_done": {"task": "Create and manage fillable forms for onboarding and compliance"}
        },
        3: {
            "challenge_info": {
                "challenge_id": "round_1b_001",
                "test_case_name": "vegetarian_corporate_catering"
            },
            "documents": [
                {"filename": "recipe_guide.pdf", "title": "Recipe Guide"}
            ],
            "persona": {"role": "Food Contractor"},
            "job_to_be_done": {"task": "Prepare vegetarian buffet-style dinner menu for corporate gathering"}
        }
    }
    
    for i, config in input_configs.items():
        input_file = Path(f"Collection {i}/challenge1b_input.json")
        with open(input_file, 'w') as f:
            json.dump(config, f, indent=2)
        print(f"   Created {input_file}")
    
    # Create dummy PDF files
    print("📄 Creating dummy PDF files...")
    dummy_content = b"%PDF-1.4\n1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n3 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] >>\nendobj\nxref\n0 4\n0000000000 65535 f \n0000000009 00000 n \n0000000058 00000 n \n0000000115 00000 n \ntrailer\n<< /Size 4 /Root 1 0 R >>\nstartxref\n174\n%%EOF"
    
    pdf_files = [
        "Collection 1/PDFs/travel_guide.pdf",
        "Collection 2/PDFs/forms_guide.pdf", 
        "Collection 3/PDFs/recipe_guide.pdf"
    ]
    
    for pdf_file in pdf_files:
        Path(pdf_file).write_bytes(dummy_content)
        print(f"   Created {pdf_file}")
    
    print("\n✅ Minimal setup complete!")
    print("\n🔄 Now run: python process_collections.py")

def check_and_install_basic_deps():
    """Check and install only the most basic dependencies."""
    print("📦 Checking basic dependencies...")
    
    try:
        import PyPDF2
        print("   ✅ PyPDF2 available")
    except ImportError:
        print("   Installing PyPDF2...")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "PyPDF2"])
    
    try:
        import pdfplumber
        print("   ✅ pdfplumber available")
    except ImportError:
        print("   Installing pdfplumber...")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pdfplumber"])

if __name__ == "__main__":
    check_and_install_basic_deps()
    create_minimal_setup()
    
    print("\n💡 Next steps:")
    print("   1. python process_collections.py")
    print("   2. python validate_outputs.py")
