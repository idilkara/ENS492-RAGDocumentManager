import os

# MongoDB configurations
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://root:example@mongodb:27017/')  # Use the container name
DB_NAME = os.getenv('DB_NAME', 'doc_db')
DOCUMENTS_COLLECTION = os.getenv('DOCUMENTS_COLLECTION', 'documents')
USERS_COLLECTION = os.getenv('USERS_COLLECTION', 'users')
SESSIONS_COLLECTION = os.getenv('SESSIONS_COLLECTION', 'sessions')

# ChromaDB configuration
CHROMADB_URL = os.getenv('CHROMADB_URL', 'http://chromadb:8000')  # Use the ChromaDB container name
CHROMADB_DIR = "db"
# Embedding Model Configuration
EMBEDDING_MODEL_URL = os.getenv('EMBEDDING_MODEL_URL', 'http://ollama:11434/v1/completions')
EMBEDDING_MODEL_NAME = os.getenv('EMBEDDING_MODEL_NAME', 'nomic-embed-text')

# Llama Model
LLAMA_MODEL = os.getenv('LLAMA_MODEL', 'mistral')  # Now configurable from env
