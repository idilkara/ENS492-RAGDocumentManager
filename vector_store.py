# vector_store.py
from history_manage import get_history, add_to_history
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
from langchain.schema import Document


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
    print(f"Processing document: {file_path}")
    if file_path.endswith(".pdf"):
        loader = PyPDFLoader(file_path)
    else:
        loader = TextLoader(file_path)

    documents = loader.load()
    print(f"Loaded {len(documents)} document(s) from {file_path}")

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    text_chunks = text_splitter.split_documents(documents)
    print(f"Split document into {len(text_chunks)} chunks")

    # Process and add documents to the vector store
    document_id = str(uuid4())
    text_chunks_with_metadata = [
        {"text": chunk.page_content, "metadata": {"document_id": document_id, "file_path": file_path}}
        for chunk in text_chunks
    ]

    documents = [
        Document(
            id=str(uuid4()),
            page_content=chunk['text'],
            metadata=chunk['metadata']
        )
        for chunk in text_chunks_with_metadata
    ]

    # Check existing document IDs
    existing_ids = set(vectorstore.get()['ids'])
    print(f"Existing IDs: {existing_ids}")

    new_documents = []
    for doc in documents:
        while doc.id in existing_ids:
            doc.id = str(uuid4())  # Generate new ID if a duplicate is found
        new_documents.append(doc)

    # Add documents to the vector store
    print(f"Adding {len(new_documents)} documents to vector store...")
    vectorstore.add_documents(new_documents)
    print(f"Added {len(new_documents)} documents successfully.")



# def list_documents():
#     """List all documents in the vector store."""
#     dblist = vectorstore.get()
#     embedded_docs = [item['source'] for item in dblist['metadatas']]
#     return embedded_docs
    
def list_documents():
    """List all documents in the vector store."""

    dblist = vectorstore.get()
    embedded_docs = [item['source'] for item in dblist['metadatas']]
    return embedded_docs


def delete_document(file_path):
    """Delete a document from the vector store and the file system."""
    # Remove the file from the file system
    if os.path.exists(file_path):
        os.remove(file_path)

    # Remove the document from the vector store
    document_id = None
    dblist = vectorstore.get()
    for item in dblist['metadatas']:
        if item['source'] == file_path:
            document_id = item['document_id']
            break

    if document_id:
        vectorstore.delete_documents([document_id])


def search_query(query):
    """Query the vector store with history context and retrieve the relevant document file path."""
    session_history = get_history()
    combined_query = "\n".join([f"User: {entry[0]}\nAgent: {entry[1]}" for entry in session_history])
    combined_query += f"\nUser: {query}"

    llm = load_model()
    qa = RetrievalQA.from_llm(llm, retriever=vectorstore.as_retriever())
    response = qa(combined_query)['result']

    combined_text = f"User Query: {query}\nAgent Response: {response}"
    relevant_file_path = get_most_relevant_doc(combined_text)

    add_to_history(query, response)
    
    print("search_query file path: ", relevant_file_path)
    
    return {"response": response, "file_path": relevant_file_path}


def get_most_relevant_doc(query):
    search_results = vectorstore.similarity_search(query)
    
    most_relevant = None
    for i in range(len(search_results)):
        most_relevant = search_results[i] 
        if search_results:
            break
        
    relevant_file_path = most_relevant.metadata.get("file_path") if most_relevant else None
    return relevant_file_path

#AAAAAAAAAAAA
# Function to retrieve documents grouped by document_id to avoid duplicates
# def retrieve_documents(query):
#     results = vectorstore.similarity_search(query)
    
#     # Group by unique document_id to avoid duplicate entries
#     unique_results = {}
#     for result in results:
#         doc_id = result.metadata["document_id"]
#         if doc_id not in unique_results:
#             unique_results[doc_id] = result
    
#     # Return only unique documents based on document_id
#     return list(unique_results.values())

def load_model():
    return ChatOllama(model="llama3.2:3b")
