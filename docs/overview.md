# Backend Module Documentation

## Overview
The backend module is the core of our system, providing the necessary services for handling chat interactions and managing vector stores. It includes several sub-modules that collectively facilitate question-answering capabilities based on retrieved documents.

## Architecture Overview
The architecture of the backend module consists of:
1. **Routes**: Handles incoming HTTP requests and routes them to appropriate endpoints.
2. **App Initialization**: Configures Flask application, sets up CORS policy, and registers blueprints.
3. **RAG Service**: Provides functionality for creating language models, managing prompt templates, and handling document retrieval.
4. **Vector Store Management**: Manages the creation, loading, and querying of vector stores used for storing and retrieving documents.
5. **Document Loader**: Loads and splits documents into manageable chunks for further processing.

Here is a high-level overview diagram showing how these components interact:
```mermaid
diagram
graph TB
    subgraph App Initialization
        app_home["app.home"]
    end
    subgraph Routes
        routes_chat["routes.chat.ask"]
    end
    subgraph RAG Service
        rag_chain_services["services.rag_service.get_rag_chain"]
        prompt_template_services["services.rag_service.get_prompt_template"]
        llm_services["services.rag_service.get_llm"]
        ask_question_services["services.rag_service.ask_question"]
    end
    subgraph Vector Store Management
        create_vector_store["services.vector_store.create_vector_store"]
        load_vector_store["services.vector_store.load_vector_store"]
        get_retriever["services.vector_store.get_retriever"]
    end
    subgraph Document Loader
        document_loader["utils.document_loader.load_documents"]
        split_documents["utils.document_loader.split_documents"]
    end

    routes_chat -->|Send Question to Service| rag_chain_services
    app_home --> routes_chat
    prompt_template_services --> llm_services
    llm_services --> ask_question_services
    create_vector_store --> load_vector_store
    load_vector_store --> get_retriever
    document_loader --> split_documents
    split_documents -->|Context for RAG Chain| rag_chain_services
```
## Sub-Modules
1. **Routes**: [routes_chat.md](./routes_chat.md)
2. **App Initialization**: [app_home.md](./app_home.md)
3. **RAG Service**: [services_rag_service.md](./services_rag_service.md)
4. **Vector Store Management**: [services_vector_store.md](./services_vector_store.md)
5. **Document Loader**: [utils_document_loader.md](./utils_document_loader.md)