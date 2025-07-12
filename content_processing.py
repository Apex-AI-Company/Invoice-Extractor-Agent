
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
            # --- START OF THE NEW, SMARTER PDF LOGIC ---
            text_from_pdf = ""
            with fitz.open(file_path) as doc:
                for page in doc:
                    text_from_pdf += page.get_text()

            # If text is found, we're done. If not, it's a scanned PDF.
            if text_from_pdf.strip():
                print("Text-based PDF detected. Extraction successful.")
                text = text_from_pdf
            else:
                # Fallback to OCR for image-based PDFs
                print("[INFO] No selectable text found. Falling back to OCR processing for the PDF...")
                ocr_text = ""
                with fitz.open(file_path) as doc:
                    for page_num, page in enumerate(doc):
                        # Convert page to a high-resolution image for better OCR
                        pix = page.get_pixmap(dpi=300)
                        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                        
                        # Perform OCR on the image of the page
                        ocr_text += pytesseract.image_to_string(img)
                        ocr_text += "\n\n--- Page End ---\n\n" # Add a separator for clarity
                text = ocr_text
            # --- END OF THE NEW PDF LOGIC ---

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

# The get_rag_context function does not need to be changed.
# It is already robust enough to handle the text output from either method.
# For simplicity, I'm omitting it here, but you should keep it in your file.
from langchain.text_splitter import RecursiveCharacterTextSplitter
from qdrant_client import QdrantClient

def get_rag_context(document_text: str, query: str) -> str:
    """Creates a temporary RAG index and retrieves relevant context for a query."""
    print("Creating dynamic RAG context...")
    if "Error:" in document_text:
      return document_text

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunks = text_splitter.split_text(document_text)

    client = QdrantClient(":memory:")
    collection_name = "dynamic_rag"
    
    try:
      client.add(collection_name=collection_name, documents=chunks, ids=list(range(len(chunks))))
    except Exception as e:
        if "sentence-transformers" in str(e) or "fastembed" in str(e):
            print("\n[INFO] 'fastembed' not found for RAG. Installing...")
            # Use sys.executable to ensure pip installs to the correct venv
            os.system(f"{sys.executable} -m pip install -q fastembed") 
            client.add(collection_name=collection_name, documents=chunks, ids=list(range(len(chunks))))
        else:
            raise e

    search_results = client.query(
        collection_name=collection_name,
        query_text=query,
        limit=3
    )
    result_texts = [hit.document for hit in search_results]
    print("RAG context retrieved successfully.")
    return "\n\n---\n\n".join(result_texts)