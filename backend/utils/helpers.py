"""
Utility Helpers Module for Image Validation, Text Cleaning, and Citation Formatting.
"""

import os
import re
from pathlib import Path
from typing import List, Union
from PIL import Image

from backend.utils.logger import get_logger

logger = get_logger()

ALLOWED_IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".bmp", ".webp"}

def validate_image_file(file_path: Union[str, Path]) -> bool:
    """
    Validates if a file exists, has a valid image extension, and can be read by PIL.
    """
    path = Path(file_path)
    if not path.exists():
        logger.error(f"Image path does not exist: {path}")
        return False

    if path.suffix.lower() not in ALLOWED_IMAGE_EXTENSIONS:
        logger.error(f"Unsupported image extension '{path.suffix}' for file: {path}")
        return False

    try:
        with Image.open(path) as img:
            img.verify()
        return True
    except Exception as e:
        logger.error(f"Corrupted or invalid image file {path}: {e}")
        return False

def clean_ocr_text(raw_text: str) -> str:
    """
    Cleans raw OCR text output by removing tab spaces, extra line breaks, and page header artifacts.
    """
    if not raw_text:
        return ""

    text = raw_text.strip()
    text = re.sub(r'[\r\t]', ' ', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r'(?i)page\s+\d+(\s+of\s+\d+)?', '', text)
    return text.strip()

def format_source_citations(docs: List[object]) -> str:
    """
    Formats retrieved LangChain Document objects into clean Markdown source citations.
    """
    if not docs:
        return "No specific NCERT textbook citations found."

    citations = []
    seen = set()
    for idx, doc in enumerate(docs, 1):
        metadata = getattr(doc, "metadata", {}) or {}
        cls = str(metadata.get("class", "NCERT")).upper()
        subject = str(metadata.get("subject", "Subject")).capitalize()
        page = metadata.get("page", "?")
        source = metadata.get("source_file", metadata.get("source", "NCERT Textbook"))
        source_name = os.path.basename(str(source))

        key = (cls, subject, source_name, page)
        if key not in seen:
            seen.add(key)
            citations.append(
                f"**[{len(seen)}] {cls} - {subject}** (File: `{source_name}`, Page: {page})"
            )

    return "\n".join(citations)
