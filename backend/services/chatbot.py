import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_classic.prompts import ChatPromptTemplate
from langchain_classic.schema.runnable import RunnablePassthrough
from langchain_classic.schema.output_parser import StrOutputParser
from langchain_classic.memory import ConversationBufferMemory

load_dotenv()

# Configuration
CHROMA_DIR = "chroma_db"
COLLECTION_NAME = "chatbot"
TOP_K = 5

def get_vector_store():
    """Connect to existing ChromaDB vector store."""
    embeddings = HuggingFaceEmbeddings(model_name = "sentence-transformers/all-MiniLM-L6-v2")
    return Chroma(
        collection_name=COLLECTION_NAME,
        persist_directory=CHROMA_DIR,
        embedding_function=embeddings
    )

def format_docs(docs):
    """Format retrieved documents into a single context string."""
    formatted = []
    for i, doc in enumerate (docs,1):
        source = doc.metadata.get("source", "Unknown")
        page = doc.metadata.get("page", "N/A")
        formatted.append(f"[Source {i}: {source}, Page {page}]\n{doc.page_content}")
    return "\n\n---\n\n".join(formatted)

# System prompt with retrieval augmented generation instructions
RAG_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are a helpful assistant that answers questions
based on the provided context. Follow these rules strictly:

1. Only answer based on the provided context
2. If the context does not contain enough information, say so
3. Cite your sources using [Source N] notation
4. Be concise but thorough
5. If asked about something outside the context, explain that
   your knowledge is limited to the provided documents

Context:
{context}"""),
    ("human", "{question}")
])

def build_rag_chain():
    """Build the complete RAG chain."""
    vector_store = get_vector_store()
    retriever = vector_store.as_retriever(
        search_type="similarity_score_threshold",
        search_kwargs={"k": TOP_K, "score_threshold" : 0.5}
    )

    llm = ChatGoogleGenerativeAI(
        model="gemma-4-31b-it",
        temperature=0.3,
        max_tokens=1024
    )

    chain = (
        {"context": retriever | format_docs,
         "question": RunnablePassthrough()}
        | RAG_PROMPT
        | llm
        | StrOutputParser()
    )

    return chain

chain = build_rag_chain()

def ask(question: str):
    return chain.invoke(question)   