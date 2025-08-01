#!/usr/bin/env python3
"""
Debug version of the processor to see exactly what's happening
"""

import json
from pathlib import Path

def debug_pdf_extraction():
    """Debug PDF extraction to see what's going wrong."""
    print("🔍 Debugging PDF extraction...")
    
    try:
        import pdfplumber
        print("✅ pdfplumber imported successfully")
    except ImportError:
        print("❌ pdfplumber not available")
        return
    
    # Check each collection
    for i in range(1, 4):
        collection_dir = Path(f"Collection {i}")
        pdf_dir = collection_dir / "PDFs"
        
        print(f"\n📁 Collection {i}:")
        print(f"   Directory exists: {collection_dir.exists()}")
        print(f"   PDFs directory exists: {pdf_dir.exists()}")
        
        if pdf_dir.exists():
            pdf_files = list(pdf_dir.glob("*.pdf"))
            print(f"   PDF files found: {len(pdf_files)}")
            
            for pdf_file in pdf_files:
                print(f"   📄 {pdf_file.name} ({pdf_file.stat().st_size} bytes)")
                
                try:
                    with pdfplumber.open(pdf_file) as pdf:
                        print(f"      Pages: {len(pdf.pages)}")
                        
                        total_text = ""
                        for page_num, page in enumerate(pdf.pages, 1):
                            page_text = page.extract_text() or ""
                            total_text += page_text
                            print(f"      Page {page_num}: {len(page_text)} characters")
                        
                        print(f"      Total text: {len(total_text)} characters")
                        print(f"      Word count: {len(total_text.split())}")
                        
                        if total_text.strip():
                            preview = total_text[:100].replace('\n', ' ').strip()
                            print(f"      Preview: '{preview}...'")
                        else:
                            print("      ⚠️  No extractable text found!")
                            
                except Exception as e:
                    print(f"      ❌ Error reading PDF: {e}")

def debug_input_files():
    """Debug input configuration files."""
    print("\n🔍 Debugging input files...")
    
    for i in range(1, 4):
        input_file = Path(f"Collection {i}/challenge1b_input.json")
        print(f"\n📄 Collection {i} input file:")
        print(f"   Exists: {input_file.exists()}")
        
        if input_file.exists():
            try:
                with open(input_file, 'r') as f:
                    data = json.load(f)
                
                print(f"   Persona: {data.get('persona', {}).get('role', 'Not found')}")
                print(f"   Task: {data.get('job_to_be_done', {}).get('task', 'Not found')}")
                print(f"   Documents: {len(data.get('documents', []))}")
                
            except Exception as e:
                print(f"   ❌ Error reading input file: {e}")

def main():
    """Run all debug checks."""
    print("🔧 Challenge 1b: Debug Analysis")
    print("=" * 40)
    
    debug_input_files()
    debug_pdf_extraction()
    
    print("\n💡 Recommendations:")
    print("1. If PDFs have no extractable text, run: python create_proper_pdfs.py")
    print("2. If you want to test with working data, run: python simple_processor.py")
    print("3. Then validate with: python validate_outputs.py")

if __name__ == "__main__":
    main()
