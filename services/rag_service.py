from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from services.vector_store import get_retriever
from config import OLLAMA_BASE_URL, OLLAMA_MODEL


def format_docs(docs):
    """Transform a list of documents into text"""
    try:
         return "\n\n".join(doc.page_content for doc in docs)
    except Exception as e:
        print(f"Error formatting document : {e}")
        return ""

def get_llm():
    """Return Ollama ll instance"""
    try:
        return ChatOllama(
            model=OLLAMA_MODEL,
            base_url=OLLAMA_BASE_URL
        )
    except Exception as e:
        print(f"Error getting llm : {e}")
        return None
    

def get_prompt_template():
    """Return prompt template for the RAG"""
    try:
        return ChatPromptTemplate.from_template(
            """
            Tu es un assistant qui répond aux questions basé sur contexte fourni.

            Contexte: {context}

            Question: {question}

            Réponds uniquement en te basant sur le contexte fourni. Si tu ne trouves pas la réponse dans le contexte, dis Je ne trouve pas cette information dans les documents fournis
            """
        )
    except Exception as e:
        print(f"Error getting prompt template : {e}")
        return None

def get_rag_chain():
    """Return the completed RAG chain"""
    try:
        retriever = get_retriever()
        prompt = get_prompt_template()
        llm = get_llm()

        chain = (
            {"context": retriever | format_docs, "question": RunnablePassthrough()}
            | prompt
            | llm
            | StrOutputParser()
        )
        return chain
    except Exception as e:
        print(f"Error getting rag chain : {e}")
        return None
    

def ask_question(question: str) -> str:
    """Ask a question and return the answer"""
    try:
        rag_chain = get_rag_chain()
        if rag_chain is None:
            return "Erreur lors de l'initialisation de la chain"

        response = rag_chain.invoke(question)
        return response
    except Exception as e:
        print(f"Error asking question: {e}")
        return f"Erreur {e}"