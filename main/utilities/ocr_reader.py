import os
import io
import fitz
import pytesseract as pt
from PIL import Image
from docx import Document
from final_project.settings import BASE_DIR

TESSERACT_CMD_PATH = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
pt.pytesseract.tesseract_cmd = TESSERACT_CMD_PATH


def pdf_to_text(pdf_path, language):
    """Convert PDF to text using PyMuPDF and Tesseract."""
    pdf_document = fitz.open(pdf_path)
    all_text = []

    for page in pdf_document:
        image_list = page.get_images(full=True)                         # Extracting images from the page
        for img_index, img in enumerate(image_list):
            xref = img[0]
            base_image = pdf_document.extract_image(xref)
            image_bytes = base_image['image']
            image = Image.open(io.BytesIO(image_bytes))                 # Converting image bytes to PIL Image
            extracted_text = pt.image_to_string(image, lang=language)   # Using Tesseract to read the image contents
            all_text.append(extracted_text)

    pdf_document.close()
    return ''.join(all_text)


def image_to_text(image_path, language):
    """Convert image to text using Tesseract."""
    image = Image.open(image_path)
    return pt.image_to_string(image, lang=language)


def create_docx(text, output_file_path):
    """Create a DOCX file from extracted text."""
    document = Document()
    document.add_paragraph(text)
    document.save(output_file_path)


def ocr_process(file_path, language):
    """Main function to extract text from PDF or JPG/PNG."""
    if file_path.endswith(('.jpg', 'jpeg', 'png')):
        extracted_text = image_to_text(file_path, language)
    else:
        extracted_text = pdf_to_text(file_path, language)

    # Define the output directory and ensure it exists
    output_directory = os.path.join(BASE_DIR, 'main', 'media', 'ocr_outputs')
    os.makedirs(output_directory, exist_ok=True)

    # Define the output file path
    output_file_path = os.path.join(BASE_DIR, 'main', 'media', 'ocr_outputs', 'processed.docx')
    create_docx(extracted_text, output_file_path)

    return output_file_path
