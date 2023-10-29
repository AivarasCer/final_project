import pytesseract as pt

TESSERACT_CMD_PATH = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
pt.pytesseract.tesseract_cmd = TESSERACT_CMD_PATH


def pdf_to_text():
    """Convert PDF to text using PyMuPDF and Tesseract."""
    pass


def image_to_text():
    """Convert image to text using Tesseract."""
    pass


def create_docx():
    """Create a DOCX file from extracted text."""
    pass


def ocr_main():
    """Main function to extract text from PDF or JPG/PNG."""
    pass
