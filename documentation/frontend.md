# Document Manager UI

## Overview
Document Manager UI is a React-based frontend application for the RAG (Retrieval-Augmented Generation) Document Management System. It provides an intuitive interface for document management, chat interactions, and PDF viewing capabilities.

## Features
- 📄 Document Management
  - Upload and manage PDF documents
  - View document list
  - Delete documents
  - PDF preview and navigation

- 💬 Chat Interface
  - Interactive chat with AI
  - Document reference highlighting
  - Multi-language support (English/Turkish)
  - Chat history management

- 🔍 Search and Retrieval
  - Semantic search across documents
  - Highlighted PDF references
  - Context-aware responses

- 👤 User Management
  - User authentication
  - Role-based access control
  - Session management




## Tech Stack
- **Core Framework**: React 18
- **Routing**: React Router DOM v6
- **PDF Handling**: 
  - @react-pdf-viewer/core
  - @react-pdf-viewer/default-layout
- **Styling**: Styled Components
- **HTTP Client**: Axios
- **Real-time Communication**: Socket.IO
- **Markdown Support**: React Markdown
- **Icons**: Lucide React

## Prerequisites
- Node.js (v14 or higher)
- npm or yarn
- Modern web browser

## Installation

1. Clone the repository:
```bash
git clone [repository-url]
cd ENS492-RAGDocumentManager/frontend/doc-manager-ui
```

2. Install dependencies:
```bash
npm install
# or
yarn install
```

## Development

Start the development server:
```bash
npm start
# or
yarn start
```

The application will be available at `http://localhost:3000`

## Building for Production - see frontend-nginx.md documentation for more detail in integration to the system for deployment

1. **Build Process**
Create a production build:
```bash
npm run build
# or
yarn build
```
   - React application is built using `npm run build`
   - Build artifacts are generated in the `build/` directory
   - These static files should then copied to the `./backend` directory

2. **Serving Architecture**
   - Nginx serves as the reverse proxy and static file server
   - Static files are served from `/usr/share/nginx/html`
   - React Router is supported through nginx configuration
   - All routes fallback to index.html for SPA functionality

3. **API Communication**
   - Frontend makes API calls to `/api/*` endpoints, the BASE URL is configured in `src/config.js`
   - Nginx proxies these requests to the Flask backend (port 5000)
   - CORS is configured to allow requests from `http://localhost:5002` which is the nginx server is serving through to the client
   - API calls are managed through `src/api.js` for header fields

### Nginx Configuration
The nginx server is configured to:
- Serve static React files
- Proxy API requests to the Flask backend
- Handle CORS and security headers
- Manage file uploads (up to 100MB)
- Configure proper caching for static assets

### API Integration
```javascript
// Example from src/config.js
const API_BASE_URL = '/api';  // Requests are proxied through nginx with neccessary fields for requests to the backend added 

// RESTful API call example using HTTP POST for document upload
// POST /api/upload - Uploads a new document
// Content-Type: multipart/form-data
// Response: 201 Created on success
const uploadDocument = async (file) => {
    const formData = new FormData();
    formData.append('file', file);
    
    const options = {
        method: 'POST',
        headers: {
            'Accept': 'application/json'
        },
        body: formData
    };

    return axios.post(`${API_BASE_URL}/upload`, formData, options);
};


## Project Structure 
doc-manager-ui/

├── public/ # Static files

├── src/ # Source code

│ ├── components/ # React components

│ ├── pages/ # Page components

│ ├── services/ # API services

│ ├── styles/ # Global styles

│ ├── utils/ # Utility functions

│ └── App.js # Root component

├── package.json # Dependencies and scripts

└── README.md # Project documentation

## Scripts for development

- `npm start`: Runs the app in development mode
- `npm test`: Launches the test runner
- `npm run build`: Builds the app for production
- `npm run eject`: Ejects from create-react-app

## Docker Support

The project includes a Dockerfile for containerization. To build and run the Docker container:

```bash
# Build the image
docker build -t doc-manager-ui .

# Run the container
docker run -p 3000:3000 doc-manager-ui
```