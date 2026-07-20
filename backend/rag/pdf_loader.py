"""
PDF Loader Module utilizing PyMuPDF (fitz) for high-performance, error-tolerant document loading.
"""

from pathlib import Path
from typing import List, Union
import fitz  # PyMuPDF

try:
    from langchain_core.documents import Document
except ImportError:
    try:
        from langchain.schema import Document
    except ImportError:
        class Document:
            def __init__(self, page_content="", metadata=None):
                self.page_content = page_content
                self.metadata = metadata or {}

from backend.utils.logger import get_logger

logger = get_logger()

def load_pdf_with_pymupdf(file_path: Union[str, Path], max_pages: int = 200) -> List[Document]:
    """
    Loads text pages from a PDF file using PyMuPDF (fitz) for fast and robust extraction.
    Ignores decompression limit issues present in standard PyPDF.
    """
    pdf_path = Path(file_path)
    if not pdf_path.exists():
        logger.error(f"PDF file does not exist: {pdf_path}")
        return []

    documents = []
    try:
        doc = fitz.open(pdf_path)
        total_pages = min(len(doc), max_pages)

        for page_num in range(total_pages):
            page = doc[page_num]
            text = page.get_text("text") or ""
            if text.strip():
                documents.append(
                    Document(
                        page_content=text,
                        metadata={
                            "page": page_num + 1,
                            "source_file": pdf_path.name,
                            "total_pages": len(doc)
                        }
                    )
                )
        doc.close()
        logger.info(f"Loaded '{pdf_path.name}' successfully ({len(documents)} text pages).")
    except Exception as e:
        logger.error(f"PyMuPDF failed to load '{pdf_path.name}': {e}")

    return documents
