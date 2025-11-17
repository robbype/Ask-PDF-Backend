import chromadb
from sentence_transformers import SentenceTransformer
from app.core.settings import PERSIST_DIR

client = chromadb.PersistentClient(path=PERSIST_DIR)
model = SentenceTransformer("all-MiniLM-L6-v2")


def split_text(text: str, chunk_size=800, overlap=100):
    from langchain_text_splitters import RecursiveCharacterTextSplitter

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=overlap, length_function=len
    )
    return splitter.split_text(text)
