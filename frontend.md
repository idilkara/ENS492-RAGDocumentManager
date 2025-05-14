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

3. Create a `.env` file in the root directory:
```env
REACT_APP_API_URL=http://localhost:5000
REACT_APP_SOCKET_URL=http://localhost:5000
```

## Development

Start the development server:
```bash
npm start
# or
yarn start
```

The application will be available at `http://localhost:3000`

## Building for Production

Create a production build:
```bash
npm run build
# or
yarn build
```

The build artifacts will be stored in the `build/` directory.

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

## Available Scripts

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