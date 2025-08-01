#!/usr/bin/env python3
"""
Test script to verify PDF files have extractable content
"""

import sys
from pathlib import Path

def test_pdf_extraction():
    """Test if we can extract text from the PDF files."""
    try:
        import pdfplumber
    except ImportError:
        print("Installing pdfplumber...")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pdfplumber"])
        import pdfplumber
    
    print("🔍 Testing PDF content extraction...")
    
    pdf_files = [
        "Collection 1/PDFs/travel_guide.pdf",
        "Collection 2/PDFs/forms_guide.pdf", 
        "Collection 3/PDFs/recipe_guide.pdf"
    ]
    
    for pdf_path in pdf_files:
        pdf_file = Path(pdf_path)
        if pdf_file.exists():
            try:
                with pdfplumber.open(pdf_file) as pdf:
                    total_text = ""
                    for page in pdf.pages:
                        text = page.extract_text() or ""
                        total_text += text
                    
                    word_count = len(total_text.split())
                    char_count = len(total_text)
                    
                    print(f"✅ {pdf_path}:")
                    print(f"   Pages: {len(pdf.pages)}")
                    print(f"   Characters: {char_count}")
                    print(f"   Words: {word_count}")
                    
                    if word_count > 50:
                        print(f"   Status: ✅ Good content")
                    else:
                        print(f"   Status: ⚠️  Limited content")
                    
                    # Show first 100 characters as preview
                    preview = total_text[:100].replace('\n', ' ').strip()
                    print(f"   Preview: {preview}...")
                    
            except Exception as e:
                print(f"❌ {pdf_path}: Error - {e}")
        else:
            print(f"❌ {pdf_path}: File not found")
    
    print("\n🎯 PDF content test completed!")

if __name__ == "__main__":
    test_pdf_extraction()
