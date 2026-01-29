📘 DocuMind AI — Intelligent Document Chat System

DocuMind AI is a local, AI-powered document assistant that allows users to upload PDF files and chat with their documents using a Retrieval-Augmented Generation (RAG) pipeline powered by Ollama and Streamlit.

It runs fully on your local machine, making it suitable for privacy-focused, offline, and low-cost AI document intelligence.

🧠 What this project does

DocuMind AI enables you to:

Upload one or more PDF documents

Automatically extract and chunk text

Generate embeddings using a local model

Retrieve relevant content based on your question

Generate accurate answers grounded only in your documents

Display source-aware responses

Interact through a clean Streamlit web interface

🏗️ System Architecture (RAG Pipeline)
PDFs → Text Extraction → Chunking → Embeddings (Ollama)
                         ↓
                    Vector Search
                         ↓
                   Relevant Chunks
                         ↓
                    Prompt Builder
                         ↓
                  Local LLM (Ollama)
                         ↓
                   Final Answer

⚙️ Tech Stack

Python 3.10+

Streamlit – web interface

Ollama – local LLM & embeddings

Mistral – response generation model

nomic-embed-text – embedding model

PyPDF2 – PDF text extraction

NumPy – vector operations

✨ Key Features

📄 Multi-PDF upload support

🔍 Context-aware document retrieval

🧩 Safe chunking to avoid context overflow

🤖 Fully local LLM (no paid APIs)

📚 Source-grounded answers

⚡ Fast, lightweight Streamlit UI

🔐 Privacy-first design

🛠️ Installation & Setup
1️⃣ Clone the repository
git clone https://github.com/shaikinzamam/DocuMind-AI.git
cd DocuMind-AI

2️⃣ Create virtual environment
python -m venv venv
venv\Scripts\activate   # Windows

3️⃣ Install dependencies
pip install -r requirements.txt

4️⃣ Install and run Ollama

Download Ollama from:
👉 https://ollama.com

Then pull the required models:

ollama pull mistral
ollama pull nomic-embed-text


Make sure Ollama is running.

5️⃣ Run the app
streamlit run app.py


Open in browser:
👉 http://localhost:8501

🧪 Example Use Cases

Study assistant for PDFs

Research paper analysis

Notes & textbook chat

Legal / policy document search

Technical manual assistant

Resume & report understanding

📌 Project Highlights (Resume-ready)

Built a local Retrieval-Augmented Generation (RAG) system to enable document-grounded AI responses.

Designed a PDF ingestion pipeline with safe chunking and embedding error handling.

Integrated Ollama local LLMs for private, offline AI inference.

Developed a Streamlit-based intelligent document chat interface.

🚧 Future Improvements

FAISS vector database integration

Page-level citation display

Chat memory & conversation summaries

OCR support for scanned PDFs

Document auto-summarization

Docker deployment

Multi-model support

👨‍💻 Author

Shaik Inzamam
B.Tech CSE (AI/ML & CS)
Aspiring AI / LLM Engineer
