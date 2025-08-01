#!/usr/bin/env python3
"""
Validation script for Challenge 1b outputs.
Fixed to work with current directory structure.
"""

import json
import sys
import os
from pathlib import Path
from typing import Dict, Any, List

def validate_output_structure(output_data: Dict[str, Any], collection_name: str) -> List[str]:
    """Validate the structure of output JSON."""
    errors = []
    
    # Check required top-level keys
    required_keys = ["metadata", "extracted_sections", "subsection_analysis"]
    for key in required_keys:
        if key not in output_data:
            errors.append(f"{collection_name}: Missing required key '{key}'")
    
    # Validate metadata
    if "metadata" in output_data:
        metadata = output_data["metadata"]
        required_metadata = ["challenge_id", "input_documents", "persona", "job_to_be_done"]
        for key in required_metadata:
            if key not in metadata:
                errors.append(f"{collection_name}: Missing metadata key '{key}'")
    
    # Validate extracted_sections
    if "extracted_sections" in output_data:
        sections = output_data["extracted_sections"]
        if not isinstance(sections, list):
            errors.append(f"{collection_name}: 'extracted_sections' must be a list")
        else:
            for i, section in enumerate(sections):
                required_section_keys = ["document", "section_title", "importance_rank", "page_number"]
                for key in required_section_keys:
                    if key not in section:
                        errors.append(f"{collection_name}: Section {i} missing key '{key}'")
    
    # Validate subsection_analysis
    if "subsection_analysis" in output_data:
        analyses = output_data["subsection_analysis"]
        if not isinstance(analyses, list):
            errors.append(f"{collection_name}: 'subsection_analysis' must be a list")
        else:
            for i, analysis in enumerate(analyses):
                required_analysis_keys = ["document", "refined_text", "page_number"]
                for key in required_analysis_keys:
                    if key not in analysis:
                        errors.append(f"{collection_name}: Analysis {i} missing key '{key}'")
    
    return errors

def find_output_files():
    """Find all output files in the current directory structure."""
    current_dir = Path(".")
    output_files = []
    
    print(f"🔍 Searching for output files in: {current_dir.absolute()}")
    
    # Look for Collection directories
    for i in range(1, 4):
        collection_dir = current_dir / f"Collection {i}"
        output_file = collection_dir / "challenge1b_output.json"
        
        print(f"   Checking: {output_file}")
        
        if output_file.exists():
            output_files.append((i, output_file))
            print(f"   ✅ Found: {output_file}")
        else:
            print(f"   ❌ Not found: {output_file}")
            
            # Check if collection directory exists
            if collection_dir.exists():
                print(f"      Collection {i} directory exists")
                # List files in the directory
                files = list(collection_dir.glob("*"))
                print(f"      Files in directory: {[f.name for f in files]}")
            else:
                print(f"      Collection {i} directory does not exist")
    
    return output_files

def validate_collection_outputs() -> bool:
    """Validate all collection outputs."""
    print("🔍 Validating Challenge 1b outputs...")
    print(f"Current working directory: {os.getcwd()}")
    
    output_files = find_output_files()
    
    if not output_files:
        print("\n❌ No output files found!")
        print("\n💡 Troubleshooting:")
        print("1. Make sure you ran: python process_collections.py")
        print("2. Check if Collection directories exist")
        print("3. Verify the processor completed successfully")
        return False
    
    all_valid = True
    
    for collection_num, output_file in output_files:
        try:
            with open(output_file, 'r', encoding='utf-8') as f:
                output_data = json.load(f)
            
            errors = validate_output_structure(output_data, f"Collection {collection_num}")
            
            if errors:
                print(f"❌ Collection {collection_num}: Validation errors:")
                for error in errors:
                    print(f"   - {error}")
                all_valid = False
            else:
                # Print summary statistics
                metadata = output_data.get("metadata", {})
                sections_count = len(output_data.get("extracted_sections", []))
                analyses_count = len(output_data.get("subsection_analysis", []))
                
                print(f"✅ Collection {collection_num}: Valid output")
                print(f"   Persona: {metadata.get('persona', 'Unknown')}")
                print(f"   Documents: {len(metadata.get('input_documents', []))}")
                print(f"   Sections: {sections_count}")
                print(f"   Analyses: {analyses_count}")
                print(f"   File size: {output_file.stat().st_size} bytes")
                
        except json.JSONDecodeError as e:
            print(f"❌ Collection {collection_num}: Invalid JSON - {e}")
            all_valid = False
        except Exception as e:
            print(f"❌ Collection {collection_num}: Error reading file - {e}")
            all_valid = False
    
    return all_valid

def show_detailed_results():
    """Show detailed results from the output files."""
    print("\n📊 Detailed Results:")
    print("=" * 50)
    
    output_files = find_output_files()
    
    for collection_num, output_file in output_files:
        try:
            with open(output_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            metadata = data.get("metadata", {})
            sections = data.get("extracted_sections", [])
            analyses = data.get("subsection_analysis", [])
            
            print(f"\n📋 Collection {collection_num} ({metadata.get('persona', 'Unknown')}):")
            print(f"   Challenge ID: {metadata.get('challenge_id', 'N/A')}")
            print(f"   Task: {metadata.get('job_to_be_done', 'N/A')}")
            print(f"   Documents processed: {metadata.get('total_documents_processed', 0)}")
            print(f"   Sections analyzed: {metadata.get('total_sections_analyzed', 0)}")
            print(f"   Processing time: {metadata.get('processing_timestamp', 'N/A')}")
            
            if sections:
                print(f"   Top sections:")
                for i, section in enumerate(sections[:3]):
                    print(f"      {i+1}. {section.get('section_title', 'N/A')} (relevance: {section.get('relevance_score', 0)})")
            
        except Exception as e:
            print(f"   ❌ Error reading Collection {collection_num}: {e}")

def main():
    """Main validation function."""
    if validate_collection_outputs():
        print("\n🎉 All outputs are valid!")
        show_detailed_results()
        sys.exit(0)
    else:
        print("\n⚠️  Some outputs failed validation")
        
        # Try to provide helpful debugging info
        print("\n🔧 Debug Information:")
        current_dir = Path(".")
        all_dirs = [d.name for d in current_dir.iterdir() if d.is_dir()]
        print(f"Available directories: {all_dirs}")
        
        all_files = [f.name for f in current_dir.rglob("*.json")]
        print(f"All JSON files found: {all_files}")
        
        sys.exit(1)

if __name__ == "__main__":
    main()
