import time
from typing import Dict, List, Optional, Tuple, Any

from backend.rag.retriever import retrieve_docs
from backend.llm.llm_engine import load_llm
from backend.ocr.vision import extract_text_from_image
from backend.utils.helpers import format_source_citations
from backend.utils.logger import get_logger

logger = get_logger()

# Singleton LLM instance
llm_engine = load_llm()

SYSTEM_TEACHER_PROMPT = """You are an expert, encouraging NCERT AI Teacher helping students from Class 5 to Class 10.

CRITICAL INSTRUCTIONS & RULES:
1. Grounding: Answer ONLY using the provided NCERT Context below. Do not use outside knowledge or hallucinate.
2. Fallback: If the answer cannot be found or logically inferred from the NCERT Context, reply exactly:
   "I could not find the answer in the provided NCERT textbook resources for your selected class and subject."
3. Style: Explain concepts step-by-step in simple, warm, clear educational language suitable for school students.
4. Structure: Use bullet points, bold key terms, and numbered steps whenever applicable.

Conversation History (Recent messages):
{chat_history}

NCERT Context:
{ncert_context}

Student Question:
{student_question}

Educational Explanation:
"""

def format_chat_history(messages: List[Dict[str, str]], max_turns: int = 6) -> str:
    """
    Formats recent session chat history for multi-turn conversational follow-ups.
    """
    if not messages:
        return "None"
    
    recent = messages[-max_turns:]
    formatted = []
    for msg in recent:
        role = "Student" if msg.get("role") == "user" else "AI Teacher"
        content = msg.get("content", "").replace("\n", " ")
        formatted.append(f"{role}: {content}")
        
    return "\n".join(formatted)

def ask_question(
    query: str,
    selected_class: Optional[str] = None,
    selected_subject: Optional[str] = None,
    session_messages: Optional[List[Dict[str, str]]] = None,
    k: int = 5
) -> Dict[str, Any]:
    """
    Processes a text doubt query through semantic search, context retrieval,
    prompt construction, and Gemma2 LLM response generation.
    """
    start_time = time.time()
    logger.info(f"Processing question: '{query}' [Class: {selected_class}, Subject: {selected_subject}]")

    if not query or not query.strip():
        return {
            "answer": "Please enter or upload a valid question.",
            "sources": "",
            "docs": [],
            "extracted_query": query
        }

    # Step 1: Semantic Context Retrieval
    docs = retrieve_docs(
        query=query,
        k=k,
        selected_class=selected_class,
        selected_subject=selected_subject
    )

    if not docs:
        logger.warning("No relevant NCERT docs retrieved for question.")
        ncert_context = "NO RELEVANT NCERT TEXTBOOK CONTENT FOUND FOR THIS QUERY."
        sources_formatted = "No matching NCERT textbook page found."
    else:
        context_blocks = []
        for idx, doc in enumerate(docs, 1):
            cls = doc.metadata.get("class", "NCERT").upper()
            sub = doc.metadata.get("subject", "Subject").capitalize()
            page = doc.metadata.get("page", "?")
            context_blocks.append(
                f"[Source {idx}: {cls} {sub}, Page {page}]\n{doc.page_content.strip()}"
            )
        ncert_context = "\n\n".join(context_blocks)
        sources_formatted = format_source_citations(docs)

    # Step 2: Format Chat History
    chat_hist_str = format_chat_history(session_messages or [])

    # Step 3: Prompt Construction
    prompt = SYSTEM_TEACHER_PROMPT.format(
        chat_history=chat_hist_str,
        ncert_context=ncert_context,
        student_question=query.strip()
    )

    # Step 4: Generate LLM Answer
    if not docs:
        answer = "I could not find the answer in the provided NCERT textbook resources for your selected class and subject."
    else:
        answer = llm_engine.generate_response(prompt)

    elapsed = time.time() - start_time
    logger.info(f"RAG doubt solving pipeline completed in {elapsed:.2f}s.")

    return {
        "answer": answer,
        "sources": sources_formatted,
        "docs": docs,
        "extracted_query": query
    }

def ask_image_question(
    image_path: str,
    selected_class: Optional[str] = None,
    selected_subject: Optional[str] = None,
    session_messages: Optional[List[Dict[str, str]]] = None
) -> Dict[str, Any]:
    """
    Processes an uploaded image doubt: runs Moondream OCR extraction and feeds
    the extracted text into the RAG pipeline.
    """
    logger.info(f"Processing image doubt from path: {image_path}")
    
    # Run Vision OCR Pipeline
    extracted_text = extract_text_from_image(image_path)
    
    if not extracted_text:
        return {
            "answer": "Could not extract clear question text from the uploaded image. Please try uploading a clearer crop or type the question directly.",
            "sources": "",
            "docs": [],
            "extracted_query": ""
        }

    # Pass extracted question text to RAG Pipeline
    result = ask_question(
        query=extracted_text,
        selected_class=selected_class,
        selected_subject=selected_subject,
        session_messages=session_messages
    )
    result["extracted_query"] = extracted_text
    return result