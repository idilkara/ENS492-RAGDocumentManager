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

# LLM Model Configuration
LLM_MODEL_NAME = os.getenv('LLM_MODEL_NAME', 'deepseek-r1:1.5b')
TOKENIZER_NAME = os.getenv('TOKENIZER_NAME', 'deepseek-ai/DeepSeek-R1-Distill-Qwen-14B')
LLM_URI = os.getenv('LLM_URI', 'http://10.3.0.96:8888/v1')

EMBEDDING_MODEL_URL = os.getenv('EMBEDDING_MODEL_URL', 'http://10.3.0.96:8888/v1/') #used to be ollama 
EMBEDDING_MODEL_NAME = os.getenv('EMBEDDING_MODEL_NAME', 'nomic-embed-text')
EMBEDDING_MODEL_NAME_V2 = "nomic-ai/nomic-embed-text-v2-moe"


# Llama Model
LLAMA_MODEL = os.getenv('LLAMA_MODEL', 'llama3.2:3b')  # Now configurable from env

LLAMA_MODEL_3_2_3B = "llama3.2:3b"
LLAMA_MODEL_3_3_70B = "llama3.3:70b"
DEEPSEEK_MODEL_R1_1_5B = "deepseek-r1:1.5b"
MISTRAL_MODEL_7B = "mistral:7b"

DEEPSEEK_TOKENIZER = "deepseek-ai/DeepSeek-R1-Distill-Qwen-14B"
DEEPSEEK_R1_MODELNAME = "DeepSeek-R1-Distill-Qwen-32B-Q6_K.ggu"


