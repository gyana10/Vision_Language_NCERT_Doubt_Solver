"""
Central Configuration Module for NCERT AI Doubt Solver.
Defines project paths, model settings, retrieval thresholds, and curriculum mappings.
"""

import os
from pathlib import Path

# Fix Windows PyTorch/OpenCV duplicate OpenMP runtime conflict
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

# Base Paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
NCERT_DIR = BASE_DIR / "ncert"
FAISS_DIR = BASE_DIR / "faiss_index"
UPLOADS_DIR = BASE_DIR / "uploads"
LOGS_DIR = BASE_DIR / "logs"

# Ensure runtime directories exist
for directory in [DATA_DIR, NCERT_DIR, FAISS_DIR, UPLOADS_DIR, LOGS_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# Vector Store & Chunking Settings
CHUNK_SIZE = 900
CHUNK_OVERLAP = 180
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

# LLM & Vision Model Settings
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
LLM_MODEL_NAME = "gemma2:2b"
VISION_MODEL_NAME = "moondream"
LLM_TEMPERATURE = 0.3

# Supported Classes & Subject Mappings
SUPPORTED_CLASSES = ["class5", "class6", "class7", "class8", "class9", "class10"]
SUBJECT_MAP = {
    "math": "maths",
    "maths": "maths",
    "sci": "science",
    "science": "science",
    "sst": "sst",
    "social": "sst",
    "studies": "sst",
    "eng": "english",
    "english": "english",
    "hin": "hindi",
    "hindi": "hindi",
    "physical": "pe",
    "phe": "pe",
    "sanskrit": "sanskrit",
    "urdu": "urdu"
}
