import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PERSIST_DIR = os.path.join(BASE_DIR, "../chroma_store")
os.makedirs(PERSIST_DIR, exist_ok=True)

HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
PDF_SAMPLE_PATH = os.path.join(BASE_DIR, "../sample.pdf")
