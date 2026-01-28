# utils_document_loader Module Documentation

## Overview
The `utils.document_loader` module provides utilities for loading and splitting documents. This is crucial in the context of a larger system where documents need to be processed before being fed into other services like vector stores or RAG chains.

## Core Functionality
This section describes the core components provided by this module, including their purpose and usage details.
### load_documents(directory_path: str)
**Purpose**: This function loads all PDF documents from a specified directory using `DirectoryLoader` and `PyPDFLoader`. It returns a list of LangChain documents ready for further processing or storage in other modules such as vector stores or RAG services.

```python
def load_documents(directory_path: str):
    # Implementation details...
```
### split_documents(documents, chunk_size=1000, chunk_overlap=200)
**Purpose**: This function takes a list of documents and splits them into smaller chunks using `RecursiveCharacterTextSplitter`. The purpose is to break down large texts or complex structures into manageable pieces that are easier to process or analyze.

```python
def split_documents(documents, chunk_size=1000, chunk_overlap=200):
    # Implementation details...
```
## Architecture and Component Relationships
The `utils.document_loader` module is part of a larger system architecture where documents are processed in stages. Here's an overview of the component relationships:
### Core Components
- **load_documents(directory_path: str)**
  - The `load_documents` function loads PDF files from a specified directory and converts them into LangChain documents.
  - This functionality is essential for initializing document processing pipelines where text extraction is required before further analysis or storage.
- **split_documents(documents, chunk_size=1000, chunk_overlap=200)**
  - The `split_documents` function splits loaded documents into smaller chunks based on specified size and overlap parameters.
  - This step ensures that the processed text data can be efficiently handled by subsequent services or models.
### Component Interaction
- **load_documents** -> **split_documents**: After loading PDF files with `load_documents`, they are typically passed to `split_documents` for further processing. Splitting into smaller chunks enables efficient handling in downstream tasks like vector store creation, RAG chain generation, and more.
### Data Flow Diagram (Mermaid)
```mermaid
graph LR;
  loadDocuments-->|documents| splitDocuments;
  splitDocuments-->|chunks| ragService;
```
## How the Module Fits into the Overall System
The `utils.document_loader` module serves as a foundational layer for document processing in a larger system. It interacts with other modules such as `services.vector_store`, where vector stores are created from processed documents, and `services.rag_service`, which uses these documents to generate prompts or RAG chains.
For more detailed information on the interaction between this module and others like services.vector_store or services.rag_service, refer to their respective documentation:

- [Vector Store Service Documentation](services_vector_store.md)
- [RAG Service Documentation](services_rag_service.md)
