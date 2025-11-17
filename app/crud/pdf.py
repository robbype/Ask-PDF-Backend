from app.core.chroma_client import client, model, split_text
import os


def process_pdf_chunks(pdf_path: str, user_id: str, document_id: int):
    from PyPDF2 import PdfReader

    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"{pdf_path} not found")

    reader = PdfReader(pdf_path)
    full_text = "".join([page.extract_text() or "" for page in reader.pages])
    chunks = split_text(full_text)

    collection_name = f"user_{user_id}_doc_{document_id}_pdf"
    collection = client.get_or_create_collection(collection_name)

    for i, chunk in enumerate(chunks):
        embedding = model.encode(chunk)
        collection.add(
            ids=[f"{os.path.basename(pdf_path)}_chunk_{i}"],
            embeddings=[embedding.tolist()],
            documents=[chunk],
        )

    return len(chunks)


def query_chroma(user_id: str, document_id: int, query_text: str, n_results=3):
    collection_name = f"user_{user_id}_doc_{document_id}_pdf"
    collection = client.get_collection(collection_name)
    embedding = model.encode(query_text)
    results = collection.query(
        query_embeddings=[embedding.tolist()],
        n_results=n_results,
        include=["documents"],
    )
    return results
