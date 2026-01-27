from  langchain_community.document_loaders import DirectoryLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pathlib import Path

def load_documents(directory_path: str):
    """
    Load all the documents on a directory
    return a list of langChain documents
    """
    documents = []
    try :
        documents = DirectoryLoader(
            path=directory_path,
            glob="**/*.pdf",
            loader_cls=PyPDFLoader
            ).load()
        return documents
    except Exception as e:
        print(f"Error during documents loading: {e}")
        return []

def split_documents(documents, chunk_size=1000, chunk_overlap=200):
    """
    Split documents into chunk
    Return a list of chunks
    """
    try:
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            is_separator_regex=False,
        )

        texts = text_splitter.split_documents(documents)
        
        return texts
    except Exception as e:
        print(f"Error during document split: {e}")
        return []