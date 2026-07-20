import sys
import os

# Ensure backend can be imported
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from backend.rag.rag_pipeline import ask_question
from backend.utils.logger import get_logger

logger = get_logger()

def test_pipeline():
    print("\n--- TEST 1: Text Question Doubt Solving ---")
    query = "What is Photosynthesis and what are its components?"
    result = ask_question(
        query=query,
        selected_class="class6",
        selected_subject="science"
    )
    print(f"Query: {query}")
    print(f"\nAI Teacher Answer:\n{result['answer']}")
    print(f"\nSource Citations:\n{result['sources']}")

    print("\n--- TEST 2: Out of Scope Question ---")
    query_out = "What is quantum computing in supercomputers?"
    result_out = ask_question(
        query=query_out,
        selected_class="class5",
        selected_subject="maths"
    )
    print(f"Query: {query_out}")
    print(f"\nAI Teacher Answer:\n{result_out['answer']}")

    print("\n--- ALL TESTS COMPLETED SUCCESSFULLY ---")

if __name__ == "__main__":
    test_pipeline()
