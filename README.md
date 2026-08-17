# AI-Powered Smart Document Analyzer & Summarizer

A full-stack document intelligence web application that ingests complex PDFs, automatically generates executive summaries, and enables context-aware conversational querying via a Retrieval-Augmented Generation (RAG) pipeline.

## Tech Stack
* **Backend:** Python, Flask
* **Database & Storage:** SQLite, Local File System
* **AI & RAG Engine:** Google Gemini API (`google-genai`), ChromaDB (Vector Search)
* **Document Parsing:** pdfplumber
* **Frontend:** HTML5, Bootstrap 5, Jinja2, Marked.js

## How It Works
1. **Extraction:** The backend parses raw text streams from uploaded PDFs page-by-page.
2. **Vectorization:** Text is chunked and embedded locally using ChromaDB to enable semantic search.
3. **RAG Pipeline:** User queries trigger semantic similarity lookups, injecting relevant document context straight into the Gemini API to prevent hallucinations and generate precise answers.
