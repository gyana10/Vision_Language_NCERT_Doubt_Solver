# 📘 NCERT Multimodal AI Doubt Solver

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://visionlanguagencertdoubtsolver.streamlit.app/)

A modern, production-ready AI-powered Educational Assistant designed for Class 5 to Class 10 students. The application solves NCERT textbook doubts using both **image-based (Vision OCR)** and **conversational text inputs**, grounded strictly in official NCERT textbook content via **Retrieval-Augmented Generation (RAG)**.

🔗 **Live Web Application**: [visionlanguagencertdoubtsolver.streamlit.app](https://visionlanguagencertdoubtsolver.streamlit.app/)

---

## 🌟 Key Features

- **🌐 Live Cloud Deployment**: Hosted live on Streamlit Cloud with pre-indexed FAISS vector store.
- **📷 Image-Based Doubt Solving**: Upload textbook screenshots, photos, or cropped questions. Uses **Moondream Vision-Language Model** (via Ollama) with automatic **EasyOCR** and **PyTesseract** fallbacks to extract question text cleanly.
- **💬 Chat-Based AI Tutor**: Type questions directly and receive step-by-step explanations written in a simple, encouraging teacher persona.
- **🔍 NCERT Grounded RAG Pipeline**: Uses **FAISS vector database** (16,602 indexed chunks) and **sentence-transformers (`all-MiniLM-L6-v2`)** to retrieve relevant textbook pages. Answers are strictly grounded in retrieved context to eliminate hallucinations.
- **🎓 Curriculum & Scope Controls**: Filter searches by **Class (Class 5 to 10)** and **Subject (Maths, Science, Social Science/SST, English, Hindi)** for targeted precision.
- **🧠 Multi-Turn Conversational Context**: Remembers session chat history to answer follow-up questions like *"Can you give an example?"* or *"Explain step 2 in detail."*
- **📚 Source Transparency & Citations**: Every answer includes clickable source citation expanders displaying the exact NCERT textbook, page number, and source file.
- **🎨 Modern Accessible UI**: Designed with WCAG compliant colors, responsive BaseWeb dropdown popovers, and smooth interactive controls.

---

## 🏗️ System Architecture

```
                          ┌──────────────────────────┐
                          │   Streamlit Frontend     │
                          │        (app.py)          │
                          └─────────────┬────────────┘
                                        │
           ┌────────────────────────────┴──────────────────────────┐
           │                                                       │
  ┌────────▼────────┐                                     ┌────────▼────────┐
  │  Text Question   │                                     │  Uploaded Image │
  └────────┬────────┘                                     └────────┬────────┘
           │                                                       │
           │                                            ┌──────────▼──────────┐
           │                                            │  Moondream OCR /    │
           │                                            │  EasyOCR Fallback   │
           │                                            └──────────┬──────────┘
           │                                                       │
           └────────────────────────────┬──────────────────────────┘
                                        │
                               ┌────────▼────────┐
                               │ Extracted Text  │
                               └────────┬────────┘
                                        │
                         ┌──────────────▼──────────────┐
                         │    RAG Pipeline Core        │
                         │(backend/rag/rag_pipeline.py)│
                         └──────────────┬──────────────┘
                                        │
                  ┌─────────────────────┴─────────────────────┐
                  │                                           │
       ┌──────────▼──────────┐                     ┌──────────▼──────────┐
       │   Embeddings &      │                     │   FAISS Vector      │
       │ SentenceTransformer │                     │      Database       │
       │ (all-MiniLM-L6-v2)  │                     │ (faiss_index/)      │
       └──────────┬──────────┘                     └──────────┬──────────┘
                  │                                           │
                  └─────────────────────┬─────────────────────┘
                                        │
                             ┌──────────▼──────────┐
                             │  Retrieved Chunks   │
                             │ (Class/Subject Filter)
                             └──────────┬──────────┘
                                        │
                             ┌──────────▼──────────┐
                             │  Gemma2 LLM Engine  │
                             │ (backend/llm/engine)│
                             └──────────┬──────────┘
                                        │
                             ┌──────────▼──────────┐
                             │ Final AI Teacher    │
                             │     Response        │
                             └─────────────────────┘
```

---

## 📁 Folder Structure

```
NCERT_Doubt_Solver/
│
├── .streamlit/
│   └── config.toml            # Native Streamlit theme config (Light Theme, WCAG compliant)
├── backend/
│   ├── llm/
│   │   ├── __init__.py
│   │   └── llm_engine.py      # Gemma2 LLM wrapper with fallback strategy
│   ├── ocr/
│   │   ├── __init__.py
│   │   └── vision.py          # Moondream VLM OCR engine & EasyOCR fallback
│   ├── rag/
│   │   ├── __init__.py
│   │   ├── embeddings.py      # SentenceTransformers lazy-loaded embeddings
│   │   ├── vector_store.py    # Document chunking, metadata attachment & FAISS index
│   │   ├── retriever.py       # Metadata-filtered similarity search
│   │   └── rag_pipeline.py    # Full RAG flow & NCERT teacher prompt engineering
│   └── utils/
│       ├── __init__.py
│       ├── logger.py          # Structured logging configuration
│       └── helpers.py         # Image validation, text cleaning & citation formatters
│
├── faiss_index/               # Pre-built FAISS vector store index (16,602 chunks)
├── uploads/                   # Temporary directory for uploaded images
├── logs/                      # Application execution log files
│
├── app.py                     # Streamlit web application frontend
├── requirements.txt           # Project Python dependencies
└── README.md                  # Project documentation
```

---

## 🚀 Quick Start & Installation

### 1. Prerequisites
- Python 3.10+ installed
- (Optional for offline LLM/Vision) [Ollama](https://ollama.com/) installed.

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Streamlit Application Locally
```bash
streamlit run app.py
```

---

## 📜 License

This project is open-source under the MIT License.
