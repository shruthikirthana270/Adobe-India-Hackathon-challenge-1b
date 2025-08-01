#!/usr/bin/env python3
"""
Adobe India Hackathon 2025 - Challenge 1b: Multi-Collection PDF Analysis
Processes multiple document collections and extracts relevant content based on personas and use cases.
"""

import json
import os
import sys
import time
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
import logging
import re
from dataclasses import dataclass
from collections import defaultdict

try:
    import PyPDF2
    import pdfplumber
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    import numpy as np
except ImportError as e:
    print(f"Error importing required libraries: {e}")
    print("Installing missing dependencies...")
    import subprocess
    
    # Try to install missing packages
    packages = ["PyPDF2", "pdfplumber", "scikit-learn", "numpy"]
    for package in packages:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        except:
            pass
    
    # Try importing again
    try:
        import PyPDF2
        import pdfplumber
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.metrics.pairwise import cosine_similarity
        import numpy as np
    except ImportError:
        print("❌ Could not install required packages. Please run:")
        print("pip install PyPDF2 pdfplumber scikit-learn numpy")
        sys.exit(1)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class PersonaContext:
    """Represents a user persona with their specific needs and context."""
    role: str
    task: str
    keywords: List[str]
    priorities: List[str]

@dataclass
class ExtractedSection:
    """Represents an extracted section from a document."""
    document: str
    section_title: str
    content: str
    page_number: int
    importance_rank: int
    relevance_score: float

@dataclass
class SubsectionAnalysis:
    """Represents refined analysis of document subsections."""
    document: str
    refined_text: str
    page_number: int
    relevance_score: float
    key_concepts: List[str]

class PersonaAnalyzer:
    """Analyzes content relevance based on user personas."""
    
    def __init__(self):
        self.persona_contexts = {
            "Travel Planner": PersonaContext(
                role="Travel Planner",
                task="Plan trips and travel experiences",
                keywords=["travel", "destination", "accommodation", "transport", "itinerary", 
                         "attractions", "restaurants", "budget", "activities", "booking"],
                priorities=["practical information", "recommendations", "logistics", "costs"]
            ),
            "HR Professional": PersonaContext(
                role="HR Professional", 
                task="Create and manage forms and compliance",
                keywords=["forms", "compliance", "onboarding", "HR", "employee", "workflow",
                         "automation", "fillable", "digital", "process"],
                priorities=["efficiency", "compliance", "automation", "user experience"]
            ),
            "Food Contractor": PersonaContext(
                role="Food Contractor",
                task="Prepare menus and catering services",
                keywords=["recipe", "menu", "vegetarian", "buffet", "catering", "ingredients",
                         "cooking", "preparation", "dietary", "corporate"],
                priorities=["scalability", "dietary restrictions", "presentation", "cost-effectiveness"]
            )
        }
    
    def get_persona_context(self, persona_role: str) -> Optional[PersonaContext]:
        """Get persona context by role."""
        return self.persona_contexts.get(persona_role)
    
    def calculate_relevance_score(self, text: str, persona: PersonaContext, task: str) -> float:
        """Calculate relevance score based on persona and task."""
        text_lower = text.lower()
        task_lower = task.lower()
        
        # Score based on keyword matches
        keyword_score = 0
        for keyword in persona.keywords:
            if keyword.lower() in text_lower:
                keyword_score += 1
        
        # Score based on task relevance
        task_words = task_lower.split()
        task_score = 0
        for word in task_words:
            if len(word) > 3 and word in text_lower:
                task_score += 1
        
        # Score based on priority matches
        priority_score = 0
        for priority in persona.priorities:
            if priority.lower() in text_lower:
                priority_score += 2
        
        # Normalize scores
        total_keywords = len(persona.keywords)
        total_task_words = len([w for w in task_words if len(w) > 3])
        total_priorities = len(persona.priorities)
        
        normalized_score = (
            (keyword_score / max(total_keywords, 1)) * 0.4 +
            (task_score / max(total_task_words, 1)) * 0.3 +
            (priority_score / max(total_priorities * 2, 1)) * 0.3
        )
        
        return min(normalized_score, 1.0)

class PDFContentExtractor:
    """Extracts and analyzes content from PDF documents."""
    
    def __init__(self):
        self.persona_analyzer = PersonaAnalyzer()
    
    def extract_text_with_structure(self, pdf_path: Path) -> Dict[str, Any]:
        """Extract structured text from PDF with section detection."""
        try:
            with pdfplumber.open(pdf_path) as pdf:
                document_data = {
                    "filename": pdf_path.name,
                    "total_pages": len(pdf.pages),
                    "sections": [],
                    "full_text": ""
                }
                
                full_text = ""
                current_section = None
                section_content = []
                
                for page_num, page in enumerate(pdf.pages, 1):
                    page_text = page.extract_text() or ""
                    full_text += page_text + "\n"
                    
                    lines = page_text.split('\n')
                    for line in lines:
                        line = line.strip()
                        if not line:
                            continue
                        
                        # Detect section headers (various patterns)
                        if self._is_section_header(line):
                            # Save previous section
                            if current_section and section_content:
                                document_data["sections"].append({
                                    "title": current_section,
                                    "content": "\n".join(section_content),
                                    "page_number": page_num,
                                    "word_count": len(" ".join(section_content).split())
                                })
                            
                            # Start new section
                            current_section = line
                            section_content = []
                        else:
                            section_content.append(line)
                
                # Add final section
                if current_section and section_content:
                    document_data["sections"].append({
                        "title": current_section,
                        "content": "\n".join(section_content),
                        "page_number": page_num,
                        "word_count": len(" ".join(section_content).split())
                    })
                
                # If no sections found, create one from full text
                if not document_data["sections"] and full_text.strip():
                    document_data["sections"].append({
                        "title": "Document Content",
                        "content": full_text.strip(),
                        "page_number": 1,
                        "word_count": len(full_text.split())
                    })
                
                document_data["full_text"] = full_text
                return document_data
                
        except Exception as e:
            logger.error(f"Error extracting from {pdf_path}: {str(e)}")
            return {
                "filename": pdf_path.name,
                "total_pages": 0,
                "sections": [{
                    "title": "Error Processing Document",
                    "content": f"Could not process PDF: {str(e)}",
                    "page_number": 1,
                    "word_count": 0
                }],
                "full_text": "",
                "error": str(e)
            }
    
    def _is_section_header(self, line: str) -> bool:
        """Detect if a line is likely a section header."""
        line = line.strip()
        
        # Skip very short or very long lines
        if len(line) < 3 or len(line) > 100:
            return False
        
        # Common header patterns
        patterns = [
            r'^[A-Z][A-Z\s]{2,}$',  # ALL CAPS
            r'^\d+\.?\s+[A-Z]',      # Numbered sections
            r'^[A-Z][a-z]+(\s[A-Z][a-z]+)*:?$',  # Title Case
            r'^[•\-\*]\s+[A-Z]',     # Bullet points with caps
            r'^\w+\s*:$',            # Single word with colon
        ]
        
        for pattern in patterns:
            if re.match(pattern, line):
                return True
        
        return False
    
    def analyze_document_relevance(self, document_data: Dict[str, Any], 
                                 persona_role: str, task: str) -> List[ExtractedSection]:
        """Analyze document sections for relevance to persona and task."""
        persona = self.persona_analyzer.get_persona_context(persona_role)
        if not persona:
            return []
        
        extracted_sections = []
        
        for section in document_data["sections"]:
            relevance_score = self.persona_analyzer.calculate_relevance_score(
                section["content"], persona, task
            )
            
            if relevance_score > 0.05:  # Include even low relevance sections
                extracted_sections.append(ExtractedSection(
                    document=document_data["filename"],
                    section_title=section["title"],
                    content=section["content"],
                    page_number=section["page_number"],
                    importance_rank=0,  # Will be set later
                    relevance_score=relevance_score
                ))
        
        # Sort by relevance and assign importance ranks
        extracted_sections.sort(key=lambda x: x.relevance_score, reverse=True)
        for i, section in enumerate(extracted_sections):
            section.importance_rank = i + 1
        
        return extracted_sections
    
    def perform_subsection_analysis(self, extracted_sections: List[ExtractedSection],
                                  persona_role: str, task: str) -> List[SubsectionAnalysis]:
        """Perform detailed analysis of extracted sections."""
        persona = self.persona_analyzer.get_persona_context(persona_role)
        if not persona:
            return []
        
        subsection_analyses = []
        
        for section in extracted_sections[:10]:  # Analyze top 10 sections
            # Extract key concepts
            key_concepts = self._extract_key_concepts(section.content, persona)
            
            # Refine text for the specific persona and task
            refined_text = self._refine_text_for_persona(section.content, persona, task)
            
            subsection_analyses.append(SubsectionAnalysis(
                document=section.document,
                refined_text=refined_text,
                page_number=section.page_number,
                relevance_score=section.relevance_score,
                key_concepts=key_concepts
            ))
        
        return subsection_analyses
    
    def _extract_key_concepts(self, text: str, persona: PersonaContext) -> List[str]:
        """Extract key concepts relevant to the persona."""
        text_lower = text.lower()
        concepts = []
        
        # Find persona-relevant keywords
        for keyword in persona.keywords:
            if keyword.lower() in text_lower:
                concepts.append(keyword)
        
        # Find priority concepts
        for priority in persona.priorities:
            if priority.lower() in text_lower:
                concepts.append(priority)
        
        # Extract important phrases (simple approach)
        sentences = text.split('.')
        for sentence in sentences[:3]:  # First few sentences often contain key info
            words = sentence.strip().split()
            if len(words) > 3:
                important_phrases = [' '.join(words[i:i+3]) for i in range(len(words)-2)]
                concepts.extend(important_phrases[:2])  # Add top 2 phrases
        
        return list(set(concepts))[:10]  # Return unique concepts, max 10
    
    def _refine_text_for_persona(self, text: str, persona: PersonaContext, task: str) -> str:
        """Refine text to be most relevant for the persona and task."""
        sentences = text.split('.')
        relevant_sentences = []
        
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue
            
            # Score sentence relevance
            score = self.persona_analyzer.calculate_relevance_score(sentence, persona, task)
            if score > 0.1:  # Include moderately relevant sentences
                relevant_sentences.append((sentence, score))
        
        # Sort by relevance and take top sentences
        relevant_sentences.sort(key=lambda x: x[1], reverse=True)
        top_sentences = [s[0] for s in relevant_sentences[:5]]
        
        return '. '.join(top_sentences) + '.' if top_sentences else text[:500]

class CollectionProcessor:
    """Main processor for handling multiple document collections."""
    
    def __init__(self, base_dir: str = "."):
        """Initialize with current directory as base."""
        self.base_dir = Path(base_dir)
        self.extractor = PDFContentExtractor()
        
        # Log the current working directory for debugging
        logger.info(f"Working directory: {os.getcwd()}")
        logger.info(f"Base directory: {self.base_dir.absolute()}")
    
    def process_collection(self, collection_path: Path) -> Dict[str, Any]:
        """Process a single collection directory."""
        logger.info(f"Processing collection: {collection_path.name}")
        
        # Load input configuration
        input_file = collection_path / "challenge1b_input.json"
        if not input_file.exists():
            logger.error(f"Input file not found: {input_file}")
            return {}
        
        with open(input_file, 'r') as f:
            input_config = json.load(f)
        
        # Extract configuration
        challenge_info = input_config.get("challenge_info", {})
        documents = input_config.get("documents", [])
        persona = input_config.get("persona", {})
        job_to_be_done = input_config.get("job_to_be_done", {})
        
        persona_role = persona.get("role", "")
        task = job_to_be_done.get("task", "")
        
        logger.info(f"Persona: {persona_role}, Task: {task}")
        
        # Process PDFs
        pdf_dir = collection_path / "PDFs"
        all_extracted_sections = []
        all_subsection_analyses = []
        processed_documents = []
        
        if pdf_dir.exists():
            pdf_files = list(pdf_dir.glob("*.pdf"))
            logger.info(f"Found {len(pdf_files)} PDF files in {pdf_dir}")
            
            for pdf_file in pdf_files:
                logger.info(f"Processing PDF: {pdf_file.name}")
                
                # Extract content
                document_data = self.extractor.extract_text_with_structure(pdf_file)
                processed_documents.append(pdf_file.name)
                
                # Analyze relevance
                extracted_sections = self.extractor.analyze_document_relevance(
                    document_data, persona_role, task
                )
                all_extracted_sections.extend(extracted_sections)
                
                # Perform subsection analysis
                subsection_analyses = self.extractor.perform_subsection_analysis(
                    extracted_sections, persona_role, task
                )
                all_subsection_analyses.extend(subsection_analyses)
        else:
            logger.warning(f"PDFs directory not found: {pdf_dir}")
        
        # Sort all sections by relevance
        all_extracted_sections.sort(key=lambda x: x.relevance_score, reverse=True)
        
        # Re-rank importance across all documents
        for i, section in enumerate(all_extracted_sections):
            section.importance_rank = i + 1
        
        # Create output
        output_data = {
            "metadata": {
                "challenge_id": challenge_info.get("challenge_id", ""),
                "test_case_name": challenge_info.get("test_case_name", ""),
                "input_documents": processed_documents,
                "persona": persona_role,
                "job_to_be_done": task,
                "processing_timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "total_sections_analyzed": len(all_extracted_sections),
                "total_documents_processed": len(processed_documents)
            },
            "extracted_sections": [
                {
                    "document": section.document,
                    "section_title": section.section_title,
                    "importance_rank": section.importance_rank,
                    "page_number": section.page_number,
                    "relevance_score": round(section.relevance_score, 3),
                    "content_preview": section.content[:200] + "..." if len(section.content) > 200 else section.content
                }
                for section in all_extracted_sections[:20]  # Top 20 sections
            ],
            "subsection_analysis": [
                {
                    "document": analysis.document,
                    "refined_text": analysis.refined_text,
                    "page_number": analysis.page_number,
                    "relevance_score": round(analysis.relevance_score, 3),
                    "key_concepts": analysis.key_concepts
                }
                for analysis in all_subsection_analyses[:15]  # Top 15 analyses
            ]
        }
        
        # Save output
        output_file = collection_path / "challenge1b_output.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Output saved to: {output_file}")
        return output_data
    
    def process_all_collections(self) -> None:
        """Process all collections in the current directory."""
        logger.info(f"Looking for collections in: {self.base_dir.absolute()}")
        
        # Look for Collection directories in current directory
        collections = [d for d in self.base_dir.iterdir() if d.is_dir() and d.name.startswith("Collection")]
        
        if not collections:
            logger.warning("No collection directories found")
            logger.info("Looking for directories that start with 'Collection'")
            # List all directories for debugging
            all_dirs = [d.name for d in self.base_dir.iterdir() if d.is_dir()]
            logger.info(f"Available directories: {all_dirs}")
            return
        
        logger.info(f"Found {len(collections)} collections to process")
        
        for collection_dir in sorted(collections):
            try:
                self.process_collection(collection_dir)
            except Exception as e:
                logger.error(f"Error processing {collection_dir.name}: {str(e)}")
        
        logger.info("All collections processed successfully")

def main():
    """Main entry point."""
    try:
        # Use current directory as base
        processor = CollectionProcessor(".")
        processor.process_all_collections()
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
