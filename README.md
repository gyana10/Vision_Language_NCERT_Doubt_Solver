# 📘 NCERT Multimodal AI Doubt Solver

A modern, production-ready AI-powered Educational Assistant designed for Class 5 to Class 10 students. The application solves NCERT textbook doubts using both **image-based (Vision OCR)** and **conversational text inputs**, grounded strictly in official NCERT textbook content via **Retrieval-Augmented Generation (RAG)**.

---

## 🌟 Key Features

- **📷 Image-Based Doubt Solving**: Upload textbook screenshots, photos, or cropped questions. Uses **Moondream Vision-Language Model** (via Ollama) with automatic **EasyOCR** fallback to extract question text cleanly.
- **💬 Chat-Based AI Tutor**: Type questions directly and receive step-by-step explanations written in a simple, encouraging teacher persona.
- **🔍 NCERT Grounded RAG Pipeline**: Uses **FAISS vector database** and **sentence-transformers (`all-MiniLM-L6-v2`)** to retrieve relevant textbook pages. Answers are strictly grounded in retrieved context to eliminate hallucinations.
- **🎓 Curriculum & Scope Controls**: Filter searches by **Class (Class 5 to 10)** and **Subject (Maths, Science, Social Science/SST, English, Hindi)** for targeted precision.
- **🧠 Multi-Turn Conversational Context**: Remembers session chat history to answer follow-up questions like *"Can you give an example?"* or *"Explain step 2 in detail."*
- **📚 Source Transparency & Citations**: Every answer includes clickable source citation expanders displaying the exact NCERT textbook, page number, and source file.
- **⚡ Offline & Robust Design**: Fully functional with local Ollama runtimes (`gemma2:2b` and `moondream`) and intelligent fallbacks for standalone or cloud execution.

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
├── data/                      # Structured NCERT textbook PDFs (Class 5 - 10)
│   ├── class5/
│   ├── class6/
│   └── ...
├── ncert/                     # Expanded NCERT textbook repository
│   ├── class 5/
│   ├── class 6/
│   └── ...
├── faiss_index/               # Saved local FAISS vector index
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
- (Optional but recommended for local LLM & Vision) [Ollama](https://ollama.com/) installed.

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. (Optional) Pull Ollama Models
If using local Ollama models:
```bash
ollama pull gemma2:2b
ollama pull moondream
```

### 4. Run the Streamlit Application
```bash
streamlit run app.py
```

---

## 🧪 Testing

Run component verification tests:
```bash
python test_ncert_solver.py
```

---

## 🔮 Future Enhancements

- [ ] **Voice Input & Text-to-Speech**: Hands-free voice queries and audio explanations for accessibility.
- [ ] **Multilingual Support**: Support for Hindi, Tamil, Telugu, and regional Indian language translations.
- [ ] **Handwritten Doubt Recognition**: Enhanced vision fine-tuning for handwritten student notebook pages.
- [ ] **Interactive Quiz Generation**: Automatically generate practice quizzes from NCERT chapter chunks.

---

## 📜 License

This project is open-source under the MIT License.
