"""
OCR & Vision Language Module supporting Moondream VLM via Ollama,
with automatic fallback to EasyOCR and PyTesseract engines.
"""

import os
import sys
import time
from pathlib import Path
from PIL import Image

# Suppress OpenMP duplicate library warnings on Windows
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

# Reconfigure stdout to UTF-8 for Windows console safety
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

from backend.config import OLLAMA_BASE_URL, VISION_MODEL_NAME
from backend.utils.logger import get_logger
from backend.utils.helpers import validate_image_file, clean_ocr_text

logger = get_logger()

# Global EasyOCR Reader Singleton
_easyocr_reader = None

def get_easyocr_reader():
    global _easyocr_reader
    # If already successfully initialized, return cached instance
    if _easyocr_reader is not None and _easyocr_reader is not False:
        return _easyocr_reader

    try:
        import easyocr
        logger.info("Initializing EasyOCR engine for image fallback...")
        _easyocr_reader = easyocr.Reader(['en'], gpu=False, verbose=False)
        return _easyocr_reader
    except Exception as e:
        logger.warning(f"EasyOCR reader initialization notice: {e}")
        _easyocr_reader = None
        return None

def extract_text_from_image(image_path: str) -> str:
    """
    Extracts question text from an uploaded textbook image using:
    1. Moondream VLM via Ollama (Primary)
    2. EasyOCR engine with 2x image upscaling (Secondary)
    3. PyTesseract engine (Tertiary)
    """
    if not validate_image_file(image_path):
        logger.error(f"Invalid image file provided to OCR: {image_path}")
        return ""

    start_time = time.time()
    logger.info(f"Starting OCR processing for image: {image_path}")
    extracted_text = ""

    # Strategy 1: Moondream VLM via Ollama
    try:
        import ollama
        client = ollama.Client(host=OLLAMA_BASE_URL)
        response = client.chat(
            model=VISION_MODEL_NAME,
            messages=[
                {
                    "role": "user",
                    "content": "Extract and transcribe all textbook question text or problem statements visible in this image.",
                    "images": [image_path]
                }
            ]
        )
        extracted_text = response.get("message", {}).get("content", "")
        if extracted_text.strip():
            logger.info("Successfully extracted text using Moondream VLM via Ollama.")
    except Exception as e:
        logger.warning(f"Ollama Moondream OCR unreachable ({e}). Switching to local EasyOCR fallback...")

    # Strategy 2: EasyOCR Engine (with 2x upscaling for small text crops)
    if not extracted_text.strip():
        reader = get_easyocr_reader()
        if reader:
            try:
                # 2x Image Upscaling for low-res screenshots
                target_path = image_path
                try:
                    with Image.open(image_path) as img:
                        w, h = img.size
                        if w < 1000 or h < 500:
                            resized = img.resize((w * 2, h * 2), Image.Resampling.LANCZOS)
                            temp_upscaled = os.path.join(os.path.dirname(image_path), "temp_ocr_upscaled.png")
                            resized.save(temp_upscaled)
                            target_path = temp_upscaled
                except Exception as resize_err:
                    logger.warning(f"Image resize notice: {resize_err}")

                results = reader.readtext(target_path, detail=0)
                extracted_text = " ".join(results)
                if extracted_text.strip():
                    logger.info(f"Successfully extracted text using EasyOCR fallback: '{extracted_text}'")
            except Exception as e:
                logger.warning(f"EasyOCR extraction attempt failed: {e}")

    # Strategy 3: PyTesseract Engine
    if not extracted_text.strip():
        try:
            import pytesseract
            with Image.open(image_path) as img:
                extracted_text = pytesseract.image_to_string(img)
                if extracted_text.strip():
                    logger.info("Successfully extracted text using PyTesseract fallback.")
        except Exception as e:
            logger.warning(f"PyTesseract extraction attempt failed: {e}")

    cleaned = clean_ocr_text(extracted_text)
    elapsed = time.time() - start_time
    logger.info(f"OCR processing finished in {elapsed:.2f}s. Extracted {len(cleaned)} characters.")
    return cleaned