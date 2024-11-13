# vector_store.py
import os
from langchain_chroma import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain.chains import RetrievalQA
from langchain_ollama import OllamaEmbeddings
from langchain_ollama import ChatOllama
from uuid import uuid4

# Constants
CHROMADB_DIR = "db"
UPLOAD_FOLDER = "upload"
EMBEDDING_MODEL_URL = "http://localhost:11434"
EMBEDDING_MODEL_NAME = "nomic-embed-text"

# Create upload folder if not exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Initialize embeddings
embeddings = OllamaEmbeddings(base_url=EMBEDDING_MODEL_URL, model=EMBEDDING_MODEL_NAME)

# Initialize vector store
vectorstore = Chroma(persist_directory=CHROMADB_DIR, embedding_function=embeddings)

def add_document(file_path):
    """Process and add a document to the vector store."""
    if file_path.endswith(".pdf"):
        loader = PyPDFLoader(file_path)
    else:
        loader = TextLoader(file_path)

    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    text_chunks = text_splitter.split_documents(documents)
    document_id = str(uuid4())  # Create a unique ID for this document
    
    # Adding metadata to each chunk to mark it with a unique document ID
    text_chunks_with_metadata = [
        {"text": chunk, "metadata": {"document_id": document_id, "file_path": file_path}}
        for chunk in text_chunks
    ]

    # Add processed documents to the vector store
    vectorstore.add_documents(text_chunks_with_metadata)

def list_documents():
    """List all documents in the vector store."""
    dblist = vectorstore.get()
    embedded_docs = [item['source'] for item in dblist['metadatas']]
    return embedded_docs

def search_query(query):
    """Query the vector store."""
    # Example retrieval, adjust as per LLM
    llm = load_model()
    qa = RetrievalQA.from_llm(llm, retriever=vectorstore.as_retriever())
    results = qa(query)
    return results['result']

# Function to retrieve documents grouped by document_id to avoid duplicates
def retrieve_documents(query):
    results = vectorstore.similarity_search(query)
    
    # Group by unique document_id to avoid duplicate entries
    unique_results = {}
    for result in results:
        doc_id = result.metadata["document_id"]
        if doc_id not in unique_results:
            unique_results[doc_id] = result
    
    # Return only unique documents based on document_id
    return list(unique_results.values())

def load_model():
    return ChatOllama(model="llama3.2:3b")
