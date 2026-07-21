import os
from dotenv import load_dotenv
load_dotenv()
TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
CHROMA_DIR = "db/chromadb" 
LLM_MODEL_NAME = "llama-3.3-70b-versatile"
VISION_MODEL_NAME = "qwen/qwen3.6-27b"
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
RETRIEVER_K = 5
RETRIEVER_SCORE_THRESHOLD = 0.3
TESSERACT_PATH = os.getenv("TESSERACT_PATH")