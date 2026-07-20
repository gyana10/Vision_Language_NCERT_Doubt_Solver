import time
from typing import List, Optional

try:
    from langchain_core.documents import Document
except ImportError:
    try:
        from langchain.schema import Document
    except ImportError:
        try:
            from langchain.docstore.document import Document
        except ImportError:
            class Document:
                def __init__(self, page_content="", metadata=None):
                    self.page_content = page_content
                    self.metadata = metadata or {}

from backend.rag.vector_store import load_vectorstore
from backend.utils.logger import get_logger

logger = get_logger()

def retrieve_docs(
    query: str,
    k: int = 5,
    selected_class: Optional[str] = None,
    selected_subject: Optional[str] = None,
    score_threshold: float = 0.25
) -> List[Document]:
    """
    Performs semantic similarity search against the FAISS vector database
    filtered by class and subject metadata.
    """
    start_time = time.time()
    logger.info(f"Retrieving docs for query: '{query}' [Class: {selected_class}, Subject: {selected_subject}]")

    vectorstore = load_vectorstore()
    if not vectorstore:
        logger.warning("Vector store unavailable for retrieval.")
        return []

    fetch_k = k * 4 if (selected_class or selected_subject) else k
    
    try:
        results_with_scores = vectorstore.similarity_search_with_relevance_scores(
            query=query,
            k=fetch_k
        )
    except Exception as e:
        logger.warning(f"Relevance score search failed ({e}); falling back to standard similarity search...")
        docs_raw = vectorstore.similarity_search(query=query, k=fetch_k)
        results_with_scores = [(doc, 1.0) for doc in docs_raw]

    filtered_docs = []
    norm_class = selected_class.lower() if selected_class else None
    norm_subject = selected_subject.lower() if selected_subject else None

    for doc, score in results_with_scores:
        doc_class = str(doc.metadata.get("class", "")).lower()
        doc_subject = str(doc.metadata.get("subject", "")).lower()

        class_match = (norm_class is None or norm_class in doc_class)
        subject_match = (norm_subject is None or norm_subject in doc_subject)

        if class_match and subject_match:
            filtered_docs.append(doc)
            if len(filtered_docs) >= k:
                break

    elapsed = time.time() - start_time
    logger.info(f"Retrieved {len(filtered_docs)} relevant NCERT chunks in {elapsed:.3f}s.")
    return filtered_docs