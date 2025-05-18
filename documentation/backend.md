# Backend Documentation

## Overview
The backend is a Flask-based REST API that implements a RAG (Retrieval-Augmented Generation) document management system. It provides functionality for document management, user authentication, and chat interactions with AI models.

## System Architecture

### Core Components
1. **Authentication System**
   - JWT-based authentication
   - Role-based access control (admin/user roles)
   - Email validation for Sabanci University domain

2. **Document Management**
   - PDF and text document processing
   - Vector store integration using ChromaDB
   - MongoDB for document storage

3. **Chat System**
   - Session-based chat management
   - Conversation history tracking
   - PDF highlighting for referenced content

### Key Technologies
- Flask (Web Framework)
- MongoDB (Document Storage)
- ChromaDB (Vector Store)
- LangChain (LLM Integration)
- PyMuPDF (PDF Processing)
- JWT (Authentication)

## API Endpoints

### Authentication
- `POST /login`
  - Authenticates users with email and password
  - Returns JWT token and user role
  - Requires @sabanciuniv.edu email

- `POST /register`
  - Creates new user accounts
  - Validates email domain and password requirements
  - Stores hashed passwords

### Document Management
- `POST /upload`
  - Uploads documents to the system
  - Processes and stores documents in both MongoDB and vector store
  - Admin-only access
  - Supports PDF files only

- `GET /get_documents`
  - Retrieves list of all stored documents
  - Returns document IDs and filenames

- `GET /get_pdf`
  - Retrieves specific document by ID
  - Returns PDF file for viewing

- `POST /delete_document`
  - Removes documents from both MongoDB and vector store
  - Admin-only access

### Chat System
- `POST /user_query`
  - Processes user queries against stored documents
  - Returns AI-generated responses with document references

- `POST /create_chat_session`
  - Creates new chat sessions
  - Initializes conversation history

- `GET /get_chat_session`
  - Retrieves existing chat session
  - Returns conversation history

- `GET /get_user_sessions`
  - Lists all chat sessions for a user

- `POST /delete_chat_session`
  - Removes specific chat session

- `POST /delete_all_chat_sessions`
  - Clears all chat sessions for a user

### PDF Highlighting
- `GET /get_highlighted_pdf`
  - Returns PDF with highlighted relevant sections
  - Used for showing document references in chat

## Vector Store Integration

### Document Processing
- Documents are split into chunks using semantic chunking
- Chunks are embedded using HuggingFace embeddings
- Stored in ChromaDB for efficient retrieval

### Search and Retrieval
- Implements contextual compression for better search results
- Uses flashrank reranking for improved relevance
- Maintains conversation context for follow-up questions

## Security Features
- JWT-based authentication
- Password hashing using bcrypt
- Role-based access control
- Email domain validation
- Secure file handling

## Configuration
The system uses environment variables for configuration: see ./backend/backend/config.py
- `MONGO_URI`: MongoDB connection string
- `DB_NAME`: Database name
- `SECRET_KEY`: JWT secret key
- `CHROMADB_URL`: ChromaDB connection URL
- `EMBEDDING_MODEL_NAME`: Name of the embedding model
- `EMBEDDING_MODEL_URL`: URL for the embedding model if it is in another server
- `LLM_MODEL_NAME`: LLM model name
- `TOKENIZER_NAME`:  tokenizer name 
- `LLM_URI`: LLM service endpoint URL to send http requests

## Error Handling
- Comprehensive error handling for file processing
- Fallback mechanisms for document processing
- Graceful error responses with appropriate HTTP status codes

## Dependencies
Some Python packages are required for the backend: see requirements.txt 

