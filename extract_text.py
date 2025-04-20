import fitz  # PyMuPDF for PDF processing
import re

def extract_text_from_pdf(pdf):
    """Extracts title and abstract from a given PDF document."""
    
    # Check if the document is empty
    if pdf.page_count == 0:
        return "Error: PDF has no pages", "Error: PDF has no pages"
    
    # Extract Title from First Page
    try:
        first_page_text = pdf[0].get_text("text")
        first_page_text_upper = first_page_text.upper()  # Convert to uppercase for case-insensitivity

        # Use regex to find title BETWEEN two known phrases
        title_match = re.search(r"A\s+FINAL\s+PROJECT\s+REPORT\s+ON\s*(.*?)\s*SUBMITTED\s+TO", first_page_text_upper, re.DOTALL)

        if title_match:
            title = title_match.group(1).strip()  # Extract title text
        else:
            title = "Title not found"
    
    except Exception as e:
        title = f"Error extracting title: {str(e)}"
    
    # Extract Abstract from 4th Page (iii in Roman Numerals)
    try:
        abstract_page = 3  # Page numbers start from 0, so 4th page is index 3
        if abstract_page >= pdf.page_count:
            abstract = "Abstract page not found"
        else:
            abstract_text = pdf[abstract_page].get_text("text")

            # Use regex to remove "Keywords" section if present
            abstract_cleaned = re.split(r"\bKEYWORDS\b", abstract_text, flags=re.IGNORECASE)[0].strip()

            abstract = abstract_cleaned if abstract_cleaned else "Abstract not found"
    except Exception as e:
        abstract = f"Error extracting abstract: {str(e)}"

    return title, abstract


