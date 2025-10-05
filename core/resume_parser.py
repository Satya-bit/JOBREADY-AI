# This file is responsible for parsing resumes from PDF or DOCX formats, extracting text.
# The flow is that if the user uploads a PDF, it first tries to extract text using PyMuPDF(fitz).
# If the text is too short or PyMuPDF fails, it falls back to OCR using Tesseract.
# So we can also handle scanned PDFs using tesseract OCR.
# For DOCX files, it uses python-docx to extract text.
#Handles different formats

import os

import docx
import fitz  
import io
from PIL import Image
import pytesseract




MIN_TEXT_LENGTH_THRESHOLD = 50 # Minimum characters to consider extraction successful without OCR

def extract_text_from_pdf_pymupdf(file_path: str) -> str | None:
    """Extracts text from a PDF file using PyMuPDF (fitz)."""
    try:
        doc = fitz.open(file_path)
        text = ""
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            text += page.get_text("text") or "" # Add null check
        doc.close()
        print(f"PyMuPDF extracted {len(text)} characters.")
        return text
    except FileNotFoundError:
        print(f"Error: PDF file not found at {file_path}")
        return None
    except Exception as e:
        print(f"Error reading PDF with PyMuPDF {file_path}: {e}")
        return None

def ocr_pdf(file_path: str) -> str | None: #for scanned PDFs(If the PDF is image and not text)
    """Extracts text from a PDF using OCR (Tesseract) as a fallback."""
    print(f"Attempting OCR on {file_path}...")
    text = ""
    try:
        doc = fitz.open(file_path)
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            # Render page to an image (pixmap)
            pix = page.get_pixmap() #bitmap image
            img_data = pix.tobytes("png") # Use PNG for lossless
            img = Image.open(io.BytesIO(img_data)) #Load it as as PIL image

            # Perform OCR on the image
            try:
                 page_text = pytesseract.image_to_string(img, lang='eng') # Specify language
                 if page_text:
                      # print(f"OCR extracted text from page {page_num + 1}") # Debugging
                      text += page_text + "\n"
                 # else:
                      # print(f"OCR found no text on page {page_num + 1}") # Debugging
            except pytesseract.TesseractNotFoundError:
                 print("\n--- Tesseract OCR Error ---")
                 print("Tesseract executable not found. Please ensure:")
                 print("1. Tesseract OCR engine is installed on your system.")
                 print("2. The 'tesseract' command is in your system's PATH.")
                 print("(On Windows, you might need to set the path manually in core/resume_parser.py)")
                 print("---------------------------\n")
                 return None # Cannot proceed without Tesseract
            except Exception as ocr_e:
                 print(f"Error during OCR processing on page {page_num + 1}: {ocr_e}")
                 # Continue to next page if one page fails

        doc.close()
        print(f"OCR extraction finished, total characters: {len(text)}")
        return text
    except FileNotFoundError:
        print(f"Error: PDF file not found for OCR at {file_path}")
        return None
    except Exception as e:
        print(f"Error opening PDF for OCR {file_path}: {e}")
        return None


def extract_text_from_docx(file_path: str) -> str | None:
    """Extracts text from a DOCX file."""
    try:
        doc = docx.Document(file_path)
        text = "\n".join([para.text for para in doc.paragraphs if para.text])
        print(f"python-docx extracted {len(text)} characters.")
        return text
    except FileNotFoundError:
        print(f"Error: DOCX file not found at {file_path}")
        return None
    except Exception as e:
        print(f"Error reading DOCX file {file_path}: {e}")
        return None


def parse_resume(file_path: str) -> str | None:
    """
    Parses resume file (PDF or DOCX).
    For PDFs, tries PyMuPDF first, then falls back to OCR if text is minimal.
    """
    _, file_extension = os.path.splitext(file_path)
    text = None

    print(f"Attempting to parse resume: {file_path}")

    if file_extension.lower() == ".pdf":
        # Try PyMuPDF first
        text = extract_text_from_pdf_pymupdf(file_path)

        # If PyMuPDF fails or gets very little text, try OCR
        if not text or len(text.strip()) < MIN_TEXT_LENGTH_THRESHOLD:
            print(f"Initial PDF text extraction yielded minimal text ({len(text or '')} chars). Falling back to OCR.")
            text_ocr = ocr_pdf(file_path)
            # Prefer OCR text only if it's significantly longer/better
            if text_ocr and len(text_ocr.strip()) > len(text or "".strip()):
                 print("Using OCR result as it seems more complete.")
                 text = text_ocr
            elif text_ocr:
                 print("OCR result not used as initial extraction was longer or OCR failed.")
                 # Stick with the (potentially short) text from PyMuPDF if OCR didn't add much
            else:
                 print("OCR attempt failed or yielded no text.")
                 # Stick with original text, even if short

    elif file_extension.lower() == ".docx":
        text = extract_text_from_docx(file_path)
    else:
        print(f"Error: Unsupported file type '{file_extension}'. Please use PDF or DOCX.")
        return None

    if text and len(text.strip()) > 0: #If there is text and it is not empty(or only contains white space)
        print(f"Resume parsed successfully. Total characters: {len(text)}")
        # Basic cleaning (optional)
        text = '\n'.join(line.strip() for line in text.splitlines() if line.strip())  # Remove leading/trailing whitespace
        return text
    else:
        print("Failed to extract meaningful text from resume after all attempts.")
        return None # Return None if even OCR fails or gets nothing substantial