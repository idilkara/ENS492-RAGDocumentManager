# RAG Document Manager Backend

## Overview
The backend is a Flask-based REST API that implements a RAG (Retrieval-Augmented Generation) document management system. It provides document processing, vector storage, and AI-powered chat capabilities.

## Features
- 📄 Document Management
  - PDF and text document processing
  - Document storage in MongoDB
  - Vector embeddings using ChromaDB
  - Document retrieval and deletion

- 🤖 AI Integration
  - Ollama integration for LLM
  - Semantic search capabilities
  - Multi-language support
  - Context-aware responses

- 🔐 Authentication
  - JWT-based authentication
  - Role-based access control
  - User session management
  - Secure password handling

- 💬 Chat System
  - Session-based chat management
  - Conversation history
  - PDF highlighting
  - Context preservation

## Tech Stack
- **Web Framework**: Flask
- **Database**: MongoDB
- **Vector Store**: ChromaDB
- **LLM Integration**: Ollama
- **Authentication**: JWT
- **Containerization**: Docker
- **Reverse Proxy**: Nginx

## Prerequisites
- Docker and Docker Compose
- Python 3.8+
- MongoDB
- ChromaDB
- Ollama

## Installation

1. Clone the repository:
```bash
git clone [repository-url]
cd ENS492-RAGDocumentManager/backend
```

2. Create a `.env` file:
```env
MONGO_URI=mongodb://root:example@mongodb:27017/
DB_NAME=doc_db
DOCUMENTS_COLLECTION=documents
USERS_COLLECTION=users
SESSIONS_COLLECTION=sessions
CHROMADB_URL=http://chromadb:8000
EMBEDDING_MODEL_URL=http://ollama:11434
EMBEDDING_MODEL_NAME=nomic-embed-text
LLAMA_MODEL=llama3.2:3b
SECRET_KEY=your-secret-key
```

3. Install Python dependencies:
```bash
pip install -r requirements.txt
```

## Running with Docker

Start all services:
```bash
docker-compose up -d
```

This will start:
- MongoDB (port 27017)
- ChromaDB (port 8001)
- Ollama (port 11434)
- Backend API (port 5001)
- Frontend (port 3000)
- Nginx (port 80)

## Project Structure
backend/
├── backend/
│ ├── app.py # Main Flask application
│ ├── vector_store.py # Vector store operations
│ ├── documents.py # Document management
│ ├── session_manager.py # Session handling
│ ├── config.py # Configuration
│ └── requirements.txt # Python dependencies
├── nginx/
│ └── nginx.conf # Nginx configuration
└── docker-compose.yml # Docker services configuration



## API Endpoints

### Authentication
- `POST /login` - User login
- `POST /register` - User registration

### Document Management
- `POST /upload` - Upload documents
- `GET /get_documents` - List all documents
- `GET /get_pdf` - Retrieve specific document
- `POST /delete_document` - Delete document

### Chat System
- `POST /user_query` - Process user queries
- `POST /create_chat_session` - Create chat session
- `GET /get_chat_session` - Retrieve chat session
- `GET /get_user_sessions` - List user sessions
- `POST /delete_chat_session` - Delete chat session

## Services Configuration

### MongoDB
```yaml
mongodb:
  image: mongo:latest
  ports:
    - "27017:27017"
  environment:
    MONGO_INITDB_ROOT_USERNAME: root
    MONGO_INITDB_ROOT_PASSWORD: example
```

### ChromaDB
```yaml
chromadb:
  image: chromadb/chroma:latest
  ports:
    - "8001:8000"
```

### Ollama
```yaml
ollama:
  image: ollama/ollama:latest
  ports:
    - "11434:11434"
```

## Development

1. Start the development server:
```bash
flask run
```

2. Run tests:
```bash
python -m pytest
```

## Security Considerations
- JWT token-based authentication
- Password hashing with bcrypt
- Role-based access control
- Secure file handling
- Input validation
- Error handling

## Performance Optimization
- Vector store indexing
- Document chunking
- Memory management
- Connection pooling
- Caching strategies

## Error Handling
- Comprehensive error catching
- Meaningful error messages
- Logging system
- Graceful degradation

