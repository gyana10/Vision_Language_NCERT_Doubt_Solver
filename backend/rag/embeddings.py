import functools
from backend.utils.logger import get_logger

logger = get_logger()

try:
    from langchain_huggingface import HuggingFaceEmbeddings
except ImportError:
    try:
        from langchain_community.embeddings import HuggingFaceEmbeddings
    except ImportError:
        try:
            from sentence_transformers import SentenceTransformer
            class HuggingFaceEmbeddings:
                def __init__(self, model_name="sentence-transformers/all-MiniLM-L6-v2", **kwargs):
                    self.model = SentenceTransformer(model_name)
                def embed_documents(self, texts):
                    return self.model.encode(texts, convert_to_numpy=True).tolist()
                def embed_query(self, text):
                    return self.model.encode(text, convert_to_numpy=True).tolist()
                def __call__(self, text):
                    return self.embed_query(text)
        except Exception as e:
            logger.error(f"No embedding framework available: {e}")
            HuggingFaceEmbeddings = None

_embeddings_instance = None

def load_embeddings():
    """
    Lazy-loads and caches the embedding model with robust multi-library fallback.
    """
    global _embeddings_instance
    if _embeddings_instance is None:
        logger.info("Loading embedding model: sentence-transformers/all-MiniLM-L6-v2...")
        try:
            if HuggingFaceEmbeddings:
                _embeddings_instance = HuggingFaceEmbeddings(
                    model_name="sentence-transformers/all-MiniLM-L6-v2"
                )
            else:
                raise ImportError("Neither langchain_huggingface nor sentence_transformers is installed.")
            logger.info("Embedding model loaded successfully.")
        except Exception as e:
            logger.error(f"Failed to load embedding model: {e}")
            raise e
            
    return _embeddings_instance