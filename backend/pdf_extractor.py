"""
PDF Text Extractor Module
File: backend/pdf_extractor.py
Description: Handles PDF text extraction
"""

import PyPDF2
import streamlit as st


class PDFTextExtractor:
    """Extract text from PDF documents"""
    
    @staticmethod
    def extract_text_from_pdf(pdf_file):
        """
        Extract text from uploaded PDF file
        
        Args:
            pdf_file: Uploaded PDF file object
            
        Returns:
            tuple: (extracted_text, total_pages) or (None, 0) if failed
        """
        try:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            text = ""
            total_pages = len(pdf_reader.pages)
            
            # Create progress bar
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Extract text from each page
            for page_num in range(total_pages):
                status_text.text(f"Extracting page {page_num + 1} of {total_pages}...")
                page = pdf_reader.pages[page_num]
                page_text = page.extract_text()
                text += page_text + "\n\n"
                progress_bar.progress((page_num + 1) / total_pages)
            
            # Clean up progress indicators
            progress_bar.empty()
            status_text.empty()
            
            return text, total_pages
            
        except PyPDF2.errors.PdfReadError:
            st.error("Error: This PDF file is corrupted or invalid.")
            return None, 0
        except Exception as e:
            st.error(f"Extraction error: {str(e)}")
            return None, 0
    
    @staticmethod
    def validate_pdf(pdf_file):
        """
        Validate if the uploaded file is a valid PDF
        
        Args:
            pdf_file: Uploaded file object
            
        Returns:
            bool: True if valid PDF, False otherwise
        """
        try:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            # Try to access first page to verify it's readable
            if len(pdf_reader.pages) > 0:
                _ = pdf_reader.pages[0]
                return True
            return False
        except Exception:
            return False
    
    @staticmethod
    def get_pdf_metadata(pdf_file):
        """
        Extract metadata from PDF
        
        Args:
            pdf_file: Uploaded PDF file object
            
        Returns:
            dict: PDF metadata
        """
        try:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            metadata = {
                'pages': len(pdf_reader.pages),
                'title': pdf_reader.metadata.get('/Title', 'Unknown') if pdf_reader.metadata else 'Unknown',
                'author': pdf_reader.metadata.get('/Author', 'Unknown') if pdf_reader.metadata else 'Unknown',
                'subject': pdf_reader.metadata.get('/Subject', 'Unknown') if pdf_reader.metadata else 'Unknown',
            }
            return metadata
        except Exception:
            return {
                'pages': 0,
                'title': 'Unknown',
                'author': 'Unknown',
                'subject': 'Unknown'
            }
    
    @staticmethod
    def extract_text_by_page(pdf_file, page_number):
        """
        Extract text from a specific page
        
        Args:
            pdf_file: Uploaded PDF file object
            page_number (int): Page number (0-indexed)
            
        Returns:
            str: Extracted text from the page
        """
        try:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            if 0 <= page_number < len(pdf_reader.pages):
                page = pdf_reader.pages[page_number]
                return page.extract_text()
            else:
                return ""
        except Exception as e:
            st.error(f"Error extracting page {page_number + 1}: {str(e)}")
            return ""
