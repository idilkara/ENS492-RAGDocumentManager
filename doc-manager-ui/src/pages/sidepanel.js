import React, { useState, useEffect } from 'react';
import './sidepanel.css';

const SidePanel = ({ isOpen }) => {
  const [message, setMessage] = useState('');
  const [searchQuery, setSearchQuery] = useState('');
  const [documents, setDocuments] = useState([]);

  useEffect(() => {
    // Simulating the fetching of document names from the 'public/pdfs' folder
    const fetchDocuments = () => {
      const pdfDocs = [
        'Project Proposal',
        'Project Plan',
        'RAG',
        'Document 1',
        'Document 2',
        'Terms and Conditions',
        'Report',
        'Document 3',
        'Aaaaaa',
        'Files',
        'Document4',
        'Document5',
      ];
      setDocuments(pdfDocs);
    };

    fetchDocuments();
  }, []);

  // Filter documents based on the search query
  const filteredDocuments = documents.filter((doc) =>
    doc.toLowerCase().includes(searchQuery.toLowerCase())
  );

  // Handlers to update the message
  const handleUploadsClick = () => {
    setMessage('Upload Document');
  };

  const handleSettingsClick = () => {
    setMessage('Settings');
  };

  const handleFileUpload = (event) => {
    const file = event.target.files[0];
    if (file && file.type === 'application/pdf') {
      setDocuments((prevDocs) => [...prevDocs, file.name]);
    } else {
      alert('Please upload a valid PDF file.');
    }
  };

  const handleLogOutClick = () => {
    // Implement logout functionality (for now, just logging out to console)
    console.log('Logged Out');
    // You can also add a redirect or clear local storage/session here.
  };

  return (
    <div className={`side-panel ${isOpen ? 'open' : ''}`}>
      <h2>Your Space</h2>

      {/* Show upload section if Upload Document is selected */}
      {message === 'Upload Document' && (
        <div className="upload-section">
          <input
            type="text"
            placeholder="Search documents..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="search-bar"
          />

          {/* File input for uploading PDFs */}
          <label htmlFor="upload-file" className="upload-button">
            Upload PDF
          </label>
          <input
            type="file"
            id="upload-file"
            accept="application/pdf"
            onChange={handleFileUpload}
          />

          <ul className="document-list">
            {filteredDocuments.map((doc, index) => (
              <li key={index} className="document-item">
                {doc}
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Settings section */}
      {message === 'Settings' && (
        <div className="settings-section">
          <div className="settings-nav">
            <div className="settings-item" onClick={handleLogOutClick}>
              Log Out
            </div>
            <div className="settings-item">
              Option 1
            </div>
            <div className="settings-item">
              Option 2
            </div>
          </div>
        </div>
      )}

      {/* Navigation bar at the bottom */}
      <div className="side-panel-nav">
        <div className="nav-item" onClick={handleUploadsClick}>Upload Document</div>
        <div className="nav-item" onClick={handleSettingsClick}>Settings</div>
      </div>
    </div>
  );
};

export default SidePanel;
