import ollama
import faiss
import numpy as np
from PyPDF2 import PdfReader
from typing import List, Tuple

class RAGSystem:
    def __init__(self):
        self.chunks = []
        self.metadata = []  # stores source + page
        self.index = None
        self.dimension = 768  # nomic-embed-text

    # ---------- PDF READING ----------
    def extract_text_from_pdf(self, pdf_path: str):
        reader = PdfReader(pdf_path)
        pages = []
        for i, page in enumerate(reader.pages):
            text = page.extract_text()
            if text:
                pages.append((text, i + 1))  # (text, page_number)
        return pages

    # ---------- CHUNKING ----------
    def chunk_text(self, text: str, chunk_size=120, overlap=30):
        words = text.split()
        chunks = []

        for i in range(0, len(words), chunk_size - overlap):
            chunk = " ".join(words[i:i + chunk_size])
            if len(chunk.strip()) > 40:
                chunks.append(chunk)

        return chunks

    # ---------- EMBEDDINGS ----------
    def embed(self, texts: List[str]):
        vectors = []
        for text in texts:
            if len(text.split()) > 300:  # low-RAM safety
                text = " ".join(text.split()[:300])

            response = ollama.embeddings(
                model="nomic-embed-text",
                prompt=text
            )
            vectors.append(response["embedding"])

        return np.array(vectors, dtype="float32")

    # ---------- PROCESS DOCUMENTS ----------
    def process_documents(self, pdf_paths: List[str]):
        all_chunks = []
        all_metadata = []

        for pdf in pdf_paths:
            pages = self.extract_text_from_pdf(pdf)
            for text, page_no in pages:
                chunks = self.chunk_text(text)
                for chunk in chunks:
                    all_chunks.append(chunk)
                    all_metadata.append({
                        "source": pdf,
                        "page": page_no
                    })

        if not all_chunks:
            raise ValueError("No readable text found in PDFs.")

        embeddings = self.embed(all_chunks)

        # FAISS index
        self.index = faiss.IndexFlatL2(self.dimension)
        self.index.add(embeddings)

        self.chunks = all_chunks
        self.metadata = all_metadata

    # ---------- RETRIEVAL ----------
    def retrieve(self, query: str, top_k=4):
        query_embedding = self.embed([query])
        distances, indices = self.index.search(query_embedding, top_k)

        results = []
        for idx in indices[0]:
            results.append({
                "text": self.chunks[idx],
                "meta": self.metadata[idx]
            })

        return results

    # ---------- PROMPT ----------
    def build_prompt(self, query: str, docs: List[dict]):
        context = ""
        for i, doc in enumerate(docs, 1):
            context += f"[Source {i}] (Page {doc['meta']['page']}):\n{doc['text']}\n\n"

        return f"""
You are DocuMind AI, an intelligent document assistant.

Answer ONLY from the context.
If the answer is not found, say:
"I don't have enough information from the document."

Context:
{context}

Question: {query}

Give a clear, structured answer.
"""

    # ---------- MAIN QUERY ----------
    def query(self, question: str):
        docs = self.retrieve(question)
        prompt = self.build_prompt(question, docs)

        response = ollama.chat(
            model="mistral",
            messages=[{"role": "user", "content": prompt}],
            options={"temperature": 0.2}
        )

        answer = response["message"]["content"]
        return answer, docs
