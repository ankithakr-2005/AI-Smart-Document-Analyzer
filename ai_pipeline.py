import os
import pdfplumber
import chromadb
from google import genai

client = genai.Client()

chroma_client = chromadb.Client()
collection = chroma_client.get_or_create_collection(name="pdf_documents")

def process_and_vectorize_pdf(file_path, doc_id):
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

    chunk_size = 500
    chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
    
    ids = [f"doc_{doc_id}_chunk_{idx}" for idx in range(len(chunks))]
    metadata = [{"doc_id": doc_id} for _ in chunks]
    
    if chunks:
        collection.add(
            documents=chunks,
            ids=ids,
            metadatas=metadata
        )
    return text[:1000]

def query_rag_pipeline(doc_id, user_query):
    results = collection.query(
        query_texts=[user_query],
        n_results=3,
        where={"doc_id": doc_id}
    )
    
    retrieved_chunks = results['documents'][0] if results['documents'] and results['documents'][0] else []
    context = "\n---\n".join(retrieved_chunks)

    prompt = f"""
    You are an expert document assistant. Answer the user's question accurately using ONLY the context provided below. 
    Use clear Markdown formatting, bullet points, and bold text where appropriate to make the answer easy to read.
    If the answer cannot be found in the context, state "I cannot find the answer in the uploaded document."
    
    Context:
    {context}
    
    User Question: {user_query}
    """

    response = client.models.generate_content(
        model='gemini-3.6-flash',
        contents=prompt
    )
    return response.text