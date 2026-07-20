"""
Structured Logging Module for NCERT AI Doubt Solver.
Logs execution, timing metrics, and exceptions to file and console.
"""

import logging
import warnings
from backend.config import LOGS_DIR

# Suppress non-critical third-party deprecation warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=UserWarning)

LOG_FILE = LOGS_DIR / "ncert_tutor.log"

logger = logging.getLogger("NCERT_AI_Tutor")
logger.setLevel(logging.INFO)

if not logger.handlers:
    # File Handler
    file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
    file_formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

    # Console Handler
    console_handler = logging.StreamHandler()
    console_formatter = logging.Formatter(
        "[%(levelname)s] %(message)s"
    )
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

def get_logger() -> logging.Logger:
    """Returns the configured logger instance."""
    return logger
