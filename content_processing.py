import os
import sys
import pytesseract
from PIL import Image
import fitz  # PyMuPDF

def extract_text_from_file(file_path: str) -> str:
    """
    Extracts text from various file types (PDF, PNG, JPG, TXT).
    For PDFs, it first tries to extract text directly. If that fails (indicating a scanned PDF),
    it falls back to performing OCR on each page.
    """
    print(f"Extracting text from '{os.path.basename(file_path)}'...")
    _, extension = os.path.splitext(file_path.lower())
    text = ""
    try:
        if extension == ".pdf":
            # Smart PDF processing with OCR fallback mech
            text_from_pdf = ""
            with fitz.open(file_path) as doc:
                for page in doc:
                    text_from_pdf += page.get_text()

            if text_from_pdf.strip():
                print("Text-based PDF detected. Extraction successful.")
                text = text_from_pdf
            else:
                print("[INFO] No selectable text found ( scaned pdf ). Falling back to OCR processing for the PDF...")
                ocr_text = ""
                with fitz.open(file_path) as doc:
                    for page_num, page in enumerate(doc):
                        pix = page.get_pixmap(dpi=300)
                        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                        ocr_text += pytesseract.image_to_string(img)
                        ocr_text += "\n\n--- Page End ---\n\n"
                text = ocr_text

        elif extension in [".png", ".jpg", ".jpeg"]:
            text = pytesseract.image_to_string(Image.open(file_path))
        elif extension == ".txt":
            with open(file_path, 'r') as f:
                text = f.read()
        else:
            return f"Unsupported file type: {extension}"

        if not text.strip():
            return "Extraction Error: No text found in the document."
        
        print("Text extraction successful.")
        return text

    except FileNotFoundError:
        return f"Error: File not found at '{file_path}'"
    except Exception as e:
        return f"An unexpected error occurred during file processing: {e}"