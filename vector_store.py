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
from langchain.schema import Document
import sqlite3

# Constants
CHROMADB_DIR = "db"
UPLOAD_FOLDER = "upload"
EMBEDDING_MODEL_URL = "http://localhost:11434"
EMBEDDING_MODEL_NAME = "nomic-embed-text"
HISTORY_SIZE = 2  # Keep only the last 2 queries and responses
GLOBAL_SESSION_ID = "global_session"  # Single global session ID

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
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    text_chunks = text_splitter.split_documents(documents)
    document_id = str(uuid4())  # Create a unique ID for this document

    # Adding metadata to each chunk to mark it with a unique document ID
    text_chunks_with_metadata = [
        {"text": chunk.page_content, "metadata": {"document_id": document_id, "file_path": file_path}}
        for chunk in text_chunks
    ]

    # Create a unique ID for each chunk
    documents = [
        Document(
            id=str(uuid4()),  # Generate a unique ID for each chunk
            page_content=chunk['text'],  # The actual content (text)
            metadata=chunk['metadata']  # Metadata containing document_id and file_path
        )
        for chunk in text_chunks_with_metadata
    ]

    # Check for existing IDs in the vector store
    existing_ids = set(vectorstore.get()['ids'])
    new_documents = []
    for doc in documents:
        while doc.id in existing_ids:
            doc.id = str(uuid4())  # Generate a new unique ID if a duplicate is found
        new_documents.append(doc)

    # Add processed documents to the vector store
    vectorstore.add_documents(new_documents)

def list_documents():
    """List all documents in the vector store."""
    dblist = vectorstore.get()
    embedded_docs = [item['source'] for item in dblist['metadatas']]
    return embedded_docs

def init_history_db():
    conn = sqlite3.connect('history.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS history (
            session_id TEXT,
            query TEXT,
            response TEXT
        )
    ''')
    conn.commit()
    conn.close()

def add_to_history(query, response):
    conn = sqlite3.connect('history.db')
    cursor = conn.cursor()

    # Remove the oldest entry if the history size exceeds the limit
    cursor.execute('SELECT COUNT(*) FROM history WHERE session_id = ?', (GLOBAL_SESSION_ID,))
    count = cursor.fetchone()[0]
    if count >= HISTORY_SIZE:
        print("HISTORY COUNT: ", count)
        cursor.execute('DELETE FROM history WHERE rowid IN (SELECT rowid FROM history WHERE session_id = ? ORDER BY rowid ASC LIMIT 1)', (GLOBAL_SESSION_ID,))

    # Add the new query and response to the history
    cursor.execute('INSERT INTO history (session_id, query, response) VALUES (?, ?, ?)',
                   (GLOBAL_SESSION_ID, query, response))
    conn.commit()
    conn.close()

def get_history():
    conn = sqlite3.connect('history.db')
    cursor = conn.cursor()
    cursor.execute('SELECT query, response FROM history WHERE session_id = ? ORDER BY rowid ASC', (GLOBAL_SESSION_ID,))
    history = cursor.fetchall()
    conn.close()
    return history

def search_query(query):
    """Query the vector store with history context."""
    # Get the history for the global session
    session_history = get_history()
    print("SESSION HIST: ", session_history)

    # Combine the history with the current query
    combined_query = "\n".join([f"User: {entry[0]}\nAgent: {entry[1]}" for entry in session_history])
    combined_query += f"\nUser: {query}"

    print("COMBINED QUERY: ", combined_query)

    # Example retrieval, adjust as per LLM
    llm = load_model()
    qa = RetrievalQA.from_llm(llm, retriever=vectorstore.as_retriever())
    results = qa(combined_query)

    # Add the query and response to the history
    add_to_history(query, results['result'])

    return results['result']

#AAAAAAAAAAAA
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

# Initialize the history database
init_history_db()