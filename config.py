import os 
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

# Configuration Ollama
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3")
# Configuration Flask
FLASK_PORT = int(os.getenv("FLASK_PORT", 5000))
# Configuration ChromaDB and document paths
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "nomic-embed-text")
DOC_PATH = Path(os.getenv("DOC_PATH", "../data/docs/"))
CHROMADB_PATH = Path(os.getenv("CHROMADB_PATH", "./chroma_db"))
