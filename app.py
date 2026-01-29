import streamlit as st
import os
import time
from rag import RAGSystem

st.set_page_config("DocuMind AI", "📘", layout="wide")

if "rag" not in st.session_state:
    st.session_state.rag = None
if "history" not in st.session_state:
    st.session_state.history = []

# ---------- SIDEBAR ----------
with st.sidebar:
    st.title("📂 DocuMind AI")
    st.caption("Local Intelligent Document Assistant")

    uploaded_files = st.file_uploader(
        "Upload PDF documents",
        type=["pdf"],
        accept_multiple_files=True
    )

    if uploaded_files and st.button("🔒 Process Documents", use_container_width=True):
        try:
            st.session_state.rag = RAGSystem()
            temp_files = []

            for file in uploaded_files:
                path = f"temp_{file.name}"
                with open(path, "wb") as f:
                    f.write(file.getbuffer())
                temp_files.append(path)

            with st.spinner("Processing documents..."):
                st.session_state.rag.process_documents(temp_files)

            for f in temp_files:
                os.remove(f)

            st.session_state.history = []
            st.success("Documents processed successfully ")

        except Exception as e:
            st.error(str(e))

    if st.session_state.history:
        if st.button("🧹 Clear chat"):
            st.session_state.history = []
            st.rerun()

# ---------- MAIN ----------
st.title("📘 DocuMind AI — Intelligent Document Chat")

for msg in st.session_state.history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Ask something about your documents..."):
    if not st.session_state.rag:
        st.error("Upload and process documents first.")
    else:
        st.session_state.history.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                answer, sources = st.session_state.rag.query(prompt)

                st.markdown(answer)

                with st.expander(" Sources"):
                    for i, src in enumerate(sources, 1):
                        st.markdown(
                            f"**Source {i}** — `{src['meta']['source']}`, page {src['meta']['page']}"
                        )

        st.session_state.history.append({"role": "assistant", "content": answer})
