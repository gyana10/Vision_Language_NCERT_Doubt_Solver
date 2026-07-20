import os
import sys

# Ensure UTF-8 output encoding for Windows terminal compatibility
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from backend.rag.vector_store import build_vectorstore
from backend.utils.logger import get_logger

logger = get_logger()

if __name__ == "__main__":
    print("==================================================")
    print("NCERT Vector Store Index Builder")
    print("==================================================")
    logger.info("Starting FAISS index build from ncert/ and data/ PDFs...")
    
    vstore = build_vectorstore()
    
    if vstore:
        print("\nSUCCESS: FAISS Vector Index created and saved in 'faiss_index/' folder!")
    else:
        print("\nWARNING: Could not build vector index. Check logs for details.")
