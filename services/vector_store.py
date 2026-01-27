from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from config import EMBEDDING_MODEL, CHROMADB_PATH, OLLAMA_BASE_URL
from utils.document_loader import load_documents, split_documents

def create_vector_store(documents_path: str):
    """
    Create a new vector from documents
    """
    try:
        # Create Embedding objet
        embeddings = OllamaEmbeddings(
            model=EMBEDDING_MODEL,
            base_url=OLLAMA_BASE_URL
        )

        # Load documents
        loaded_documents = load_documents(directory_path=documents_path)
        splited_documents = split_documents(documents=loaded_documents)

        # Create vectore store
        vector_store = Chroma.from_documents(
            collection_name="documents",
            embedding=embeddings,
            documents=splited_documents,
            persist_directory=str(CHROMADB_PATH)
        )
    except Exception as e:
        print(f"Error during vector store creating: {e}")

def load_vector_store():
    """
    Load existing vector store
    """
    try:

        # Create Embedding objet
        embeddings = OllamaEmbeddings(
            model=EMBEDDING_MODEL,
            base_url=OLLAMA_BASE_URL
        )

        # Create vectore store
        vector_store = Chroma(
            collection_name="documents",
            embedding_function=embeddings,
            persist_directory=str(CHROMADB_PATH)
        )
        return vector_store
    except Exception as e:
        print(f"Error during vector store loading: {e}")
        return None

def get_retriever(k=5):
    """
    Return a retriever to search the most k pertinents documents
    """
    try:
        vector_store = load_vector_store()
        retriever = vector_store.as_retriever(search_kwargs={"k": k})
        return retriever
    except Exception as e:
        print(f"Error during retriever creation: {e}")
        return None