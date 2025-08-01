#!/usr/bin/env python3
"""
Local runner for Challenge 1b without Docker
Automatically installs dependencies and runs the processor
"""

import subprocess
import sys
import os
from pathlib import Path

def install_dependencies():
    """Install dependencies using the auto installer."""
    print("📦 Installing dependencies...")
    
    try:
        # Run the auto installer
        result = subprocess.run([sys.executable, "auto_install_deps.py"], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Dependencies installed successfully")
            return True
        else:
            print(f"❌ Dependency installation failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error installing dependencies: {e}")
        return False

def run_processor():
    """Run the collection processor locally."""
    print("🔄 Running collection processor...")
    
    try:
        # Change to the correct directory
        os.chdir(Path(__file__).parent)
        
        # Run the processor
        result = subprocess.run([sys.executable, "process_collections.py"], 
                              capture_output=False, text=True)
        
        if result.returncode == 0:
            print("✅ Processing completed successfully")
            return True
        else:
            print("❌ Processing failed")
            return False
            
    except Exception as e:
        print(f"❌ Error running processor: {e}")
        return False

def validate_outputs():
    """Validate the generated outputs."""
    print("🔍 Validating outputs...")
    
    try:
        result = subprocess.run([sys.executable, "validate_outputs.py"], 
                              capture_output=True, text=True)
        
        print(result.stdout)
        
        if result.returncode == 0:
            print("✅ Validation completed successfully")
            return True
        else:
            print("⚠️  Some validation issues found")
            return False
            
    except Exception as e:
        print(f"❌ Error validating outputs: {e}")
        return False

def main():
    """Main execution function."""
    print("🚀 Challenge 1b: Local Runner")
    print("=" * 30)
    
    # Install dependencies
    if not install_dependencies():
        print("\n💡 Try installing manually:")
        print("   pip install PyPDF2 pdfplumber scikit-learn numpy scipy nltk textblob pandas tqdm")
        sys.exit(1)
    
    print()
    
    # Run processor
    if not run_processor():
        print("\n❌ Processing failed. Check error messages above.")
        sys.exit(1)
    
    print()
    
    # Validate outputs
    validate_outputs()
    
    print("\n🎉 Challenge 1b completed!")
    print("\n📁 Check the following files for results:")
    for i in range(1, 4):
        output_file = f"Collection {i}/challenge1b_output.json"
        if Path(output_file).exists():
            print(f"   ✅ {output_file}")
        else:
            print(f"   ❌ {output_file} (not found)")

if __name__ == "__main__":
    main()
