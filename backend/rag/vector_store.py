"""
Vector Store Module for Document Ingestion, Chunking, and FAISS Vector Database Management.
"""

import os
import time
from pathlib import Path
from typing import List, Optional

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

from backend.config import (
    DATA_DIR,
    NCERT_DIR,
    FAISS_DIR,
    CHUNK_SIZE,
    CHUNK_OVERLAP,
    SUBJECT_MAP
)
from backend.rag.pdf_loader import load_pdf_with_pymupdf
from backend.rag.embeddings import load_embeddings
from backend.utils.logger import get_logger

logger = get_logger()

def normalize_class_name(raw_name: str) -> str:
    """Normalizes folder names like 'class 5' or 'class5' into 'class5'."""
    return raw_name.lower().replace(" ", "")

def normalize_subject_name(filename: str) -> str:
    """Normalizes PDF filenames into standardized subject keys (e.g., maths, science, sst)."""
    name = filename.replace(".pdf", "").lower()
    for key, val in SUBJECT_MAP.items():
        if key in name:
            return val
    return name.split()[0]

def load_ncert_documents() -> List[Document]:
    """
    Scans 'ncert/' and 'data/' directories for Class 5 to Class 10 PDFs,
    attaching normalized metadata to each page.
    """
    all_documents = []
    scan_paths = [NCERT_DIR, DATA_DIR]
    loaded_count = 0

    for base_path in scan_paths:
        if not base_path.exists():
            continue
        logger.info(f"Scanning directory for NCERT PDFs: {base_path}")
        for class_dir in sorted(base_path.iterdir()):
            if class_dir.is_dir() and "class" in class_dir.name.lower():
                norm_class = normalize_class_name(class_dir.name)
                for pdf_file in class_dir.glob("*.pdf"):
                    norm_subject = normalize_subject_name(pdf_file.name)
                    docs = load_pdf_with_pymupdf(pdf_file)
                    for doc in docs:
                        doc.metadata["class"] = norm_class
                        doc.metadata["subject"] = norm_subject
                        doc.metadata["source_file"] = pdf_file.name
                        doc.metadata["chapter"] = f"{norm_subject.capitalize()} Section"
                    all_documents.extend(docs)
                    loaded_count += 1

    logger.info(f"Loaded total {loaded_count} PDF books ({len(all_documents)} pages total).")
    return all_documents

def chunk_documents(documents: List[Document]) -> List[Document]:
    """Splits loaded page documents into chunks using RecursiveCharacterTextSplitter."""
    try:
        from langchain_text_splitters import RecursiveCharacterTextSplitter
    except ImportError:
        from langchain.text_splitter import RecursiveCharacterTextSplitter

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", ". ", " ", ""]
    )
    chunks = splitter.split_documents(documents)
    logger.info(f"Generated {len(chunks)} text chunks (size: {CHUNK_SIZE}, overlap: {CHUNK_OVERLAP}).")
    return chunks

def build_vectorstore() -> Optional[object]:
    """Builds the FAISS vector index from scratch and persists it to disk."""
    start_time = time.time()
    logger.info("Starting FAISS vector store build...")
    
    documents = load_ncert_documents()
    if not documents:
        logger.warning("No NCERT documents found to index.")
        return None

    chunks = chunk_documents(documents)
    embeddings = load_embeddings()

    try:
        from langchain_community.vectorstores import FAISS
    except ImportError:
        from langchain.vectorstores import FAISS

    logger.info(f"Creating FAISS vector index from {len(chunks)} chunks...")
    vectorstore = FAISS.from_documents(chunks, embeddings)
    FAISS_DIR.mkdir(parents=True, exist_ok=True)
    vectorstore.save_local(str(FAISS_DIR))
    
    elapsed = time.time() - start_time
    logger.info(f"FAISS index built and persisted to '{FAISS_DIR}' in {elapsed:.2f}s.")
    return vectorstore

def load_vectorstore() -> Optional[object]:
    """Loads the persisted FAISS vector index from disk. Automatically builds if missing."""
    index_file = FAISS_DIR / "index.faiss"
    if not index_file.exists():
        logger.info("FAISS index file not found. Triggering automatic build...")
        return build_vectorstore()

    try:
        try:
            from langchain_community.vectorstores import FAISS
        except ImportError:
            from langchain.vectorstores import FAISS

        logger.info(f"Loading existing FAISS index from {FAISS_DIR}...")
        embeddings = load_embeddings()
        vectorstore = FAISS.load_local(
            str(FAISS_DIR),
            embeddings,
            allow_dangerous_deserialization=True
        )
        logger.info("FAISS vector store loaded successfully.")
        return vectorstore
    except Exception as e:
        logger.error(f"Error loading FAISS vector store: {e}. Rebuilding index...")
        return build_vectorstore()

if __name__ == "__main__":
    build_vectorstore()