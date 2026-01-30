# Document Loader Utilities Module

## Introduction

The `document_loader_utilities` module is part of the document processing pipeline and its primary responsibility is to load documents from a specified directory and split them into smaller chunks for further processing. It relies on two core functions: `load_documents` and `split_documents`, both of which are detailed below.

# Architecture Overview

The `document_loader_utilities` module is designed to work seamlessly with other modules in the document processing pipeline. Specifically, it integrates with the following components:

- **Dependency on `vector_store`**: The documents loaded and split by this module are often used as inputs for vector stores that help in indexing and retrieving relevant document chunks.
- **Integration with `rag_service`**: After splitting documents into smaller chunks, these pieces of text might be fed to the RAG (Retrieval-Augmented Generation) service where they can be processed further by language models or stored for future retrieval.
# Architecture Overview

The `document_loader_utilities` module is designed to work seamlessly with other modules in the document processing pipeline. Specifically, it integrates with the following components:

- **Dependency on `vector_store`**: The documents loaded and split by this module are often used as inputs for vector stores that help in indexing and retrieving relevant document chunks.
  - [vector_store](./vector_store.md) provides functionality to create, load, and retrieve from a vector store where the loaded and split documents can be stored and retrieved efficiently. It also interacts with services.vector_store.get_retriever, which helps fetch specific information based on queries or patterns.

- **Integration with `rag_service`**: After splitting documents into smaller chunks, these pieces of text might be fed to the RAG (Retrieval-Augmented Generation) service where they can be processed further by language models or stored for future retrieval. The interaction primarily involves services.rag_service.get_rag_chain, which builds a chain that combines document retrieval with question answering using a large language model.

### Core Components

### Core Components
## Core Components

### 1. Loading Documents (`utils.document_loader.load_documents(directory_path)`) 

#### Function Description
The `load_documents` function takes a directory path as input and loads all PDF documents within that directory using the `DirectoryLoader` class from `langchain_community.document_loaders`. This loader supports loading multiple files based on a glob pattern. The loaded documents are returned as a list of LangChain-compatible document objects.

#### Parameters
- **directory_path**: A string specifying the path to the directory containing the PDF documents to be loaded.

#### Returns
A list of LangChain document objects representing the loaded documents.

#### Exceptions Handled
If an error occurs during the loading process, a generic exception is caught and printed. An empty list is returned in case of failure.

### 2. Splitting Documents (`utils.document_loader.split_documents(documents)`) 

#### Function Description
The `split_documents` function takes a list of documents as input and splits them into smaller chunks based on the specified chunk size and overlap using the `RecursiveCharacterTextSplitter` class from `langchain_text_splitters`. The resulting text chunks are returned.

#### Parameters
- **documents**: A list of document objects loaded by the `load_documents` function or other similar methods. 
- **chunk_size**: (Optional) An integer representing the size of each chunk to be split, defaulting to 1000 characters if not specified.
- **chunk_overlap**: (Optional) An integer representing the overlap between chunks in terms of character count, defaulting to 200 if not specified.

#### Returns 
A list of text strings representing the smaller document chunks.

#### Exceptions Handled
If an error occurs during the splitting process, a generic exception is caught and printed. An empty list is returned in case of failure.