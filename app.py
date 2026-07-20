import os
import time
import streamlit as st

from backend.rag.rag_pipeline import ask_question, ask_image_question
from backend.rag.vector_store import build_vectorstore
from backend.utils.logger import get_logger

logger = get_logger()

# Streamlit Page Configuration
st.set_page_config(
    page_title="NCERT AI Multimodal Tutor",
    page_icon="📘",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Header Component
st.title("📘 NCERT Multimodal AI Tutor")
st.caption("Grounded educational doubt solver for Class 5 to 10 powered by RAG, FAISS & Moondream OCR")

# Session State Initialization
if "messages" not in st.session_state:
    st.session_state.messages = []

# SIDEBAR CONTROLS
st.sidebar.title("⚙️ Curriculum Controls")

# Class Selector
selected_class_raw = st.sidebar.selectbox(
    "🎓 Select Class",
    [
        "All Classes",
        "Class 5",
        "Class 6",
        "Class 7",
        "Class 8",
        "Class 9",
        "Class 10"
    ]
)
selected_class = None if selected_class_raw == "All Classes" else selected_class_raw.lower().replace(" ", "")

# Subject Selector
selected_subject_raw = st.sidebar.selectbox(
    "📖 Select Subject",
    [
        "All Subjects",
        "Science",
        "Maths",
        "Social Science (SST)",
        "English",
        "Hindi"
    ]
)
selected_subject = None
if selected_subject_raw != "All Subjects":
    if "sst" in selected_subject_raw.lower():
        selected_subject = "sst"
    else:
        selected_subject = selected_subject_raw.lower()

st.sidebar.markdown("---")

# Image Upload Section
st.sidebar.subheader("📷 Upload Textbook Image")
uploaded_image = st.sidebar.file_uploader(
    "Upload question screenshot or photo",
    type=["png", "jpg", "jpeg"]
)

process_image_btn = False
if uploaded_image:
    st.sidebar.image(uploaded_image, caption="Uploaded Doubt Image", use_container_width=True)
    process_image_btn = st.sidebar.button("🔍 Solve Image Doubt", type="primary")

st.sidebar.markdown("---")

# Re-Index Button
if st.sidebar.button("🔄 Re-build Vector Index"):
    with st.spinner("Indexing NCERT textbooks..."):
        vstore = build_vectorstore()
        if vstore:
            st.sidebar.success("FAISS Vector Store updated successfully!")
        else:
            st.sidebar.error("Failed to build vector store.")

# Clear Chat Button
if st.sidebar.button("🗑️ Clear Conversation"):
    st.session_state.messages = []
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.info("""
**System Architecture:**
- **OCR:** Moondream / EasyOCR
- **Embeddings:** all-MiniLM-L6-v2
- **Vector DB:** FAISS
- **LLM:** Gemma2 via Ollama / Teacher Engine
""")

# Display Active Filters Info
st.info(f"**Active Filters:** Class: `{selected_class_raw}` | Subject: `{selected_subject_raw}` | Grounded NCERT Mode")

# Image Doubt Handler with Streamlit Seek(0) Fix
if uploaded_image and process_image_btn:
    try:
        temp_dir = "uploads"
        os.makedirs(temp_dir, exist_ok=True)
        temp_image_path = os.path.join(temp_dir, uploaded_image.name)

        # Fix: Reset byte buffer cursor to start before reading
        uploaded_image.seek(0)
        image_bytes = uploaded_image.getvalue()

        with open(temp_image_path, "wb") as f:
            f.write(image_bytes)

        logger.info(f"Saved uploaded image {uploaded_image.name} ({len(image_bytes)} bytes) to {temp_image_path}")

        with st.spinner("Extracting question text using Moondream Vision OCR..."):
            result = ask_image_question(
                image_path=temp_image_path,
                selected_class=selected_class,
                selected_subject=selected_subject,
                session_messages=st.session_state.messages
            )

        extracted_query = result.get("extracted_query", "")
        answer = result.get("answer", "")
        sources = result.get("sources", "")

        user_msg = f"📷 [Image Uploaded] {extracted_query}"
        st.session_state.messages.append({"role": "user", "content": user_msg})
        st.session_state.messages.append({
            "role": "assistant",
            "content": answer,
            "sources": sources
        })
        st.rerun()
    except Exception as e:
        st.error(f"Image Processing Error: {e}")
        logger.error(f"Error processing uploaded image: {e}")

# Render Chat History
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("sources"):
            with st.expander("📚 Source NCERT Textbook Pages"):
                st.markdown(msg["sources"])

# Text Doubt Input Handler
user_query = st.chat_input("Type your NCERT doubt question here (e.g., Explain Photosynthesis step by step)...")

if user_query:
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.markdown(user_query)

    with st.chat_message("assistant"):
        with st.spinner("Searching NCERT textbooks and formulating explanation..."):
            try:
                result = ask_question(
                    query=user_query,
                    selected_class=selected_class,
                    selected_subject=selected_subject,
                    session_messages=st.session_state.messages
                )
                answer = result.get("answer", "")
                sources = result.get("sources", "")

                st.markdown(answer)
                if sources:
                    with st.expander("📚 Source NCERT Textbook Pages"):
                        st.markdown(sources)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer,
                    "sources": sources
                })
            except Exception as e:
                err_msg = f"An error occurred while solving your doubt: {e}"
                st.error(err_msg)
                logger.error(f"RAG execution failure: {e}")