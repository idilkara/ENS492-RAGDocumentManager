import React, { useState } from 'react';
import './documentManagement.css';

const DocumentManagement = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedDocument, setSelectedDocument] = useState(null);

  const documents = [
    { id: 1, name: 'ECON 400 - Lecture 1.pdf' },
    { id: 2, name: 'ECON 400 - Lecture 2.pdf' },
    { id: 3, name: 'Jeremy Bentham Notes.pdf' },
    { id: 4, name: 'Richard Cantillon Essay.pdf' },
    { id: 5, name: 'Population Theory.pdf' }
  ];

  const filteredDocuments = documents.filter(doc =>
    doc.name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const handleSearch = (e) => {
    setSearchTerm(e.target.value);
  };

  const handleSelectDocument = (doc) => {
    setSelectedDocument(doc.id);
  };

  return (
    <div className="document-management-container">
      <div className="document-header">Documents</div>
      <input
        type="text"
        placeholder="Search documents..."
        value={searchTerm}
        onChange={handleSearch}
        className="search-input"
      />
      <div className="document-list">
        {filteredDocuments.map(doc => (
          <div
            key={doc.id}
            className={`document-item ${selectedDocument === doc.id ? 'selected' : ''}`}
            onClick={() => handleSelectDocument(doc)}
          >
            {doc.name}
          </div>
        ))}
      </div>
    </div>
  );
};

export default DocumentManagement;
