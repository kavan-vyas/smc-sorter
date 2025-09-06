#!/usr/bin/env python3
"""
Web Page to PDF Converter with GIF Support (ReportLab Version)

This script converts web pages to PDFs with embedded GIF questions and answers.
It expects a specific folder structure with GIF files named as 1234.gif (questions) 
and 1234s.gif (answers).

Requirements:
- pip install reportlab pillow

Folder structure:
main.py
questions_folder/
    ├── 1234.gif (question)
    ├── 1234s.gif (answer)
    ├── 5678.gif (question)
    ├── 5678s.gif (answer)
    └── ...
"""

import os
import sys
from pathlib import Path
from typing import List, Tuple, Optional

try:
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.utils import ImageReader
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch, cm
    from reportlab.lib import colors
    from PIL import Image as PILImage
except ImportError as e:
    print(f"Missing required packages. Please install with:")
    print("pip install reportlab pillow")
    sys.exit(1)


class WebPageToPDFConverter:
    """Converts web pages to PDFs with embedded GIF questions and answers."""
    
    def __init__(self, questions_folder: str = "questions_folder"):
        """
        Initialize the converter.
        
        Args:
            questions_folder: Path to folder containing GIF files
        """
        self.questions_folder = Path(questions_folder)
        self.output_folder = Path("output_pdfs")
        self.output_folder.mkdir(exist_ok=True)
        
        # PDF settings
        self.page_width, self.page_height = A4
        self.margin = 2 * cm
        self.content_width = self.page_width - 2 * self.margin
        self.content_height = self.page_height - 2 * self.margin
        
    def get_gif_pairs(self) -> List[Tuple[str, str, str]]:
        """
        Get all question-answer GIF pairs from the folder.
        
        Returns:
            List of tuples (question_id, question_path, answer_path)
        """
        if not self.questions_folder.exists():
            print(f"Error: Questions folder '{self.questions_folder}' not found!")
            return []
            
        gif_pairs = []
        
        # Find all question GIFs (those without 's' suffix)
        question_gifs = list(self.questions_folder.glob("*.gif"))
        
        for question_gif in question_gifs:
            filename = question_gif.stem
            
            # Skip answer GIFs (those ending with 's')
            if filename.endswith('s'):
                continue
                
            # Look for corresponding answer GIF
            answer_gif = self.questions_folder / f"{filename}s.gif"
            
            if answer_gif.exists():
                gif_pairs.append((filename, str(question_gif), str(answer_gif)))
            else:
                print(f"Warning: No answer found for question {filename}")
                
        return sorted(gif_pairs)
    
    def get_image_dimensions(self, image_path: str, max_width: float = None, max_height: float = None) -> Tuple[float, float]:
        """
        Get optimal dimensions for image while maintaining aspect ratio.
        
        Args:
            image_path: Path to image file
            max_width: Maximum width in points
            max_height: Maximum height in points
            
        Returns:
            Tuple of (width, height) in points
        """
        if max_width is None:
            max_width = self.content_width - 2 * cm
        if max_height is None:
            max_height = (self.content_height - 4 * cm) / 2  # Half page minus margins
            
        try:
            with PILImage.open(image_path) as img:
                img_width, img_height = img.size
                aspect_ratio = img_width / img_height
                
                # Calculate dimensions that fit within constraints
                if img_width > img_height:
                    # Landscape orientation
                    width = min(max_width, img_width)
                    height = width / aspect_ratio
                    if height > max_height:
                        height = max_height
                        width = height * aspect_ratio
                else:
                    # Portrait orientation
                    height = min(max_height, img_height)
                    width = height * aspect_ratio
                    if width > max_width:
                        width = max_width
                        height = width / aspect_ratio
                        
                return width, height
                
        except Exception as e:
            print(f"Error getting image dimensions for {image_path}: {e}")
            return max_width * 0.8, max_height * 0.8
    
    def create_pdf_with_gifs(self, question_path: str, answer_path: str, 
                           question_id: str, output_path: str) -> bool:
        """
        Create PDF with question and answer GIFs using ReportLab.
        
        Args:
            question_path: Path to question GIF
            answer_path: Path to answer GIF
            question_id: Question identifier
            output_path: Output PDF file path
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Create PDF document
            doc = SimpleDocTemplate(
                output_path,
                pagesize=A4,
                rightMargin=self.margin,
                leftMargin=self.margin,
                topMargin=self.margin,
                bottomMargin=self.margin
            )
            
            # Create styles
            styles = getSampleStyleSheet()
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=24,
                spaceAfter=30,
                alignment=1,  # Center alignment
                textColor=colors.HexColor('#333333')
            )
            
            section_style = ParagraphStyle(
                'CustomSection',
                parent=styles['Heading2'],
                fontSize=18,
                spaceAfter=20,
                spaceBefore=30,
                alignment=1,  # Center alignment
                textColor=colors.HexColor('#555555')
            )
            
            id_style = ParagraphStyle(
                'IDStyle',
                parent=styles['Normal'],
                fontSize=14,
                spaceAfter=20,
                alignment=1,  # Center alignment
                textColor=colors.HexColor('#666666')
            )
            
            # Build content
            content = []
            
            # Title and question ID
            content.append(Paragraph("Question", title_style))
            content.append(Paragraph(f"Question ID: {question_id}", id_style))
            
            # Question image
            try:
                q_width, q_height = self.get_image_dimensions(question_path)
                question_img = Image(question_path, width=q_width, height=q_height)
                question_img.hAlign = 'CENTER'
                content.append(question_img)
            except Exception as e:
                print(f"Error adding question image: {e}")
                content.append(Paragraph(f"[Question image could not be loaded: {question_path}]", styles['Normal']))
            
            # Spacer between sections
            content.append(Spacer(1, 40))
            
            # Separator line
            content.append(Paragraph('<para align="center">─────────────────────────────────</para>', styles['Normal']))
            
            # Answer section
            content.append(Paragraph("Answer", section_style))
            
            # Answer image
            try:
                a_width, a_height = self.get_image_dimensions(answer_path)
                answer_img = Image(answer_path, width=a_width, height=a_height)
                answer_img.hAlign = 'CENTER'
                content.append(answer_img)
            except Exception as e:
                print(f"Error adding answer image: {e}")
                content.append(Paragraph(f"[Answer image could not be loaded: {answer_path}]", styles['Normal']))
            
            # Build PDF
            doc.build(content)
            print(f"✓ Created PDF: {output_path}")
            return True
            
        except Exception as e:
            print(f"Error creating PDF {output_path}: {e}")
            return False
    
    def create_simple_pdf(self, question_path: str, answer_path: str, 
                         question_id: str, output_path: str) -> bool:
        """
        Create PDF using direct canvas approach for maximum compatibility.
        
        Args:
            question_path: Path to question GIF
            answer_path: Path to answer GIF
            question_id: Question identifier
            output_path: Output PDF file path
            
        Returns:
            True if successful, False otherwise
        """
        try:
            c = canvas.Canvas(output_path, pagesize=A4)
            width, height = A4
            
            # Title
            c.setFont("Helvetica-Bold", 24)
            c.drawCentredText(width/2, height - 80, "Question")
            
            # Question ID
            c.setFont("Helvetica", 14)
            c.drawCentredText(width/2, height - 110, f"Question ID: {question_id}")
            
            # Question image
            try:
                q_width, q_height = self.get_image_dimensions(
                    question_path, 
                    max_width=width - 4*cm,
                    max_height=(height - 200) / 2.2
                )
                
                q_x = (width - q_width) / 2
                q_y = height - 150 - q_height
                
                c.drawImage(question_path, q_x, q_y, width=q_width, height=q_height)
                
                # Answer section - positioned below question image
                answer_y_start = q_y - 80
                
            except Exception as e:
                print(f"Error with question image: {e}")
                answer_y_start = height / 2
            
            # Separator line
            line_y = answer_y_start + 30
            c.line(width/2 - 100, line_y, width/2 + 100, line_y)
            
            # Answer title
            c.setFont("Helvetica-Bold", 18)
            c.drawCentredText(width/2, answer_y_start, "Answer")
            
            # Answer image
            try:
                a_width, a_height = self.get_image_dimensions(
                    answer_path,
                    max_width=width - 4*cm,
                    max_height=answer_y_start - 100
                )
                
                a_x = (width - a_width) / 2
                a_y = answer_y_start - 40 - a_height
                
                c.drawImage(answer_path, a_x, a_y, width=a_width, height=a_height)
                
            except Exception as e:
                print(f"Error with answer image: {e}")
                c.setFont("Helvetica", 12)
                c.drawCentredText(width/2, answer_y_start - 60, f"[Answer image error: {str(e)}]")
            
            c.save()
            print(f"✓ Created PDF: {output_path}")
            return True
            
        except Exception as e:
            print(f"Error creating simple PDF {output_path}: {e}")
            return False
    
    def process_all_questions(self, use_simple_mode: bool = False) -> None:
        """
        Process all question-answer pairs and create PDFs.
        
        Args:
            use_simple_mode: If True, use simple canvas-based PDF creation
        """
        gif_pairs = self.get_gif_pairs()
        
        if not gif_pairs:
            print("No question-answer pairs found!")
            return
            
        print(f"Found {len(gif_pairs)} question-answer pairs")
        successful_conversions = 0
        
        for question_id, question_path, answer_path in gif_pairs:
            print(f"\nProcessing question {question_id}...")
            
            output_path = self.output_folder / f"question_{question_id}.pdf"
            
            # Try advanced mode first, fall back to simple mode
            if use_simple_mode:
                success = self.create_simple_pdf(question_path, answer_path, question_id, str(output_path))
            else:
                success = self.create_pdf_with_gifs(question_path, answer_path, question_id, str(output_path))
                if not success:
                    print("  Retrying with simple mode...")
                    success = self.create_simple_pdf(question_path, answer_path, question_id, str(output_path))
            
            if success:
                successful_conversions += 1
                
        print(f"\n{'='*50}")
        print(f"Conversion complete!")
        print(f"Successfully created {successful_conversions}/{len(gif_pairs)} PDFs")
        print(f"Output folder: {self.output_folder.absolute()}")
    
    def process_single_question(self, question_id: str, use_simple_mode: bool = False) -> bool:
        """
        Process a single question-answer pair.
        
        Args:
            question_id: The question identifier (e.g., "1234")
            use_simple_mode: If True, use simple canvas-based PDF creation
            
        Returns:
            True if successful, False otherwise
        """
        question_path = self.questions_folder / f"{question_id}.gif"
        answer_path = self.questions_folder / f"{question_id}s.gif"
        
        if not question_path.exists():
            print(f"Error: Question GIF not found: {question_path}")
            return False
            
        if not answer_path.exists():
            print(f"Error: Answer GIF not found: {answer_path}")
            return False
            
        print(f"Processing question {question_id}...")
        
        output_path = self.output_folder / f"question_{question_id}.pdf"
        
        if use_simple_mode:
            return self.create_simple_pdf(str(question_path), str(answer_path), question_id, str(output_path))
        else:
            success = self.create_pdf_with_gifs(str(question_path), str(answer_path), question_id, str(output_path))
            if not success:
                print("  Retrying with simple mode...")
                success = self.create_simple_pdf(str(question_path), str(answer_path), question_id, str(output_path))
            return success


def main():
    """Main function to run the converter."""
    print("Web Page to PDF Converter with GIF Support (ReportLab)")
    print("Creates ONE combined PDF with all questions in ascending order")
    print("=" * 65)
    
    # Check if questions folder exists
    questions_folder = "questions_folder"
    use_simple_mode = False
    
    args = sys.argv[1:]
    
    # Parse arguments
    if "--simple" in args:
        use_simple_mode = True
        args.remove("--simple")
        print("Using simple PDF generation mode")
    
    if len(args) > 0:
        questions_folder = args[0]
    
    converter = WebPageToPDFConverter(questions_folder)
    
    if len(args) > 1:
        # Process single question (keeping this for testing individual questions)
        question_id = args[1]
        success = converter.process_single_question(question_id, use_simple_mode)
        if success:
            print(f"✓ Successfully created PDF for question {question_id}")
        else:
            print(f"✗ Failed to create PDF for question {question_id}")
    else:
        # Process ALL questions into ONE combined PDF
        print("Processing all questions into a single combined PDF...")
        converter.process_all_questions(use_simple_mode)


if __name__ == "__main__":
    main()