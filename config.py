#config.py

import os

# MongoDB configuration
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
DB_NAME = 'doc_db'
DOCUMENTS_COLLECTION = 'documents'
USERS_COLLECTION = 'users'
SESSIONS_COLLECTION = 'sessions'

# ChromaDB configuration
CHROMADB_DIR = "db"
EMBEDDING_MODEL_URL = "http://localhost:11434"
EMBEDDING_MODEL_NAME = "nomic-embed-text"

LLAMA_MODEL_3_2_3B = "llama3.2:3b"
LLAMA_MODEL_3_3_70B = "llama3.3:70b"
DEEPSEEK_MODEL_R1_1_5B = "deepseek-r1:1.5b"
MISTRAL_MODEL_7B = "mistral:7b"

