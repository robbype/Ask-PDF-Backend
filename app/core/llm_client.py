from huggingface_hub import InferenceClient
from app.core.settings import HUGGINGFACE_API_KEY

client_llm = InferenceClient(api_key=HUGGINGFACE_API_KEY)
