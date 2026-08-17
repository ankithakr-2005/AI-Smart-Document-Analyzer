# AI-Powered Smart Document Analyzer & Summarizer

A full-stack document intelligence web application that ingests complex PDFs, automatically generates professional executive summaries upon upload, and enables context-aware conversational querying via a Retrieval-Augmented Generation (RAG) pipeline.

---

## Key Features
* **Automatic Summarization:** Instantly generates and pre-loads a structured executive summary the moment a PDF is uploaded.
* **Context-Aware RAG Chat:** Allows users to interactively question the document without AI hallucinations, backed by strict grounding prompts.
* **Semantic Vector Search:** Utilizes local vector embeddings via ChromaDB to search documents by meaning rather than simple keywords.
* **Persistent History:** Relational tracking of documents and chat histories using SQLite.
* **Modern SaaS UI:** Features a sleek, responsive dark-and-light theme built with Bootstrap 5 and client-side Markdown rendering via Marked.js.

---

## Tech Stack
* **Backend:** Python, Flask, Werkzeug
* **Database:** SQLite (Relational metadata & chat history)
* **Vector Database & AI:** ChromaDB, Google Gemini API (`google-genai` SDK using `gemini-3.6-flash`)
* **Document Parsing:** pdfplumber
* **Frontend:** HTML5, Bootstrap 5, Jinja2, Marked.js

---

## ⚙️ How the RAG Pipeline Works
1. **Ingestion & Parsing:** Raw text streams are extracted page-by-page from the uploaded PDF using `pdfplumber`.
2. **Chunking & Vectorization:** Text is sliced into semantic chunks and embedded into **ChromaDB**.
3. **Retrieval & Grounding:** User queries trigger similarity lookups. The most relevant chunks are injected as context into the Gemini API, ensuring answers are derived strictly from the source document.
