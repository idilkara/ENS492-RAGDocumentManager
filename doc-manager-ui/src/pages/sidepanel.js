import React, { useState, useEffect } from 'react';
import './sidepanel.css';

const SidePanel = ({ isOpen }) => {
  const [message, setMessage] = useState('');
  const [searchQuery, setSearchQuery] = useState('');
  const [documents, setDocuments] = useState([]);
  const [isUploading, setIsUploading] = useState(false);  // State to track uploading process
  const [selectedItem, setSelectedItem] = useState("settings"); // State to track the selected item


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
    setSelectedItem("uploads");

  };

  const handleSettingsClick = () => {
    setMessage('Settings');
    setSelectedItem("settings");
  };

  const handleFileUpload = async (event) => {
    const file = event.target.files[0];
    console.log("File selected:", file);
  
    if (file && file.type === 'application/pdf') {
      try {
        setIsUploading(true);  // Start uploading state
        console.log('Uploading started...');
  
        const formData = new FormData();
        formData.append('file', file);
  
        const response = await fetch('http://127.0.0.1:5000/upload', {
          method: 'POST',
          body: formData,
        });
  
        const result = await response.json();
        console.log('Upload result:', result);
  
        if (response.ok) {
          setDocuments((prevDocs) => [...prevDocs, file.name]);
          alert(result.message);  // Show success message
        } else {
          alert(result.error || 'Error uploading the file');  // Show error message
        }
      } catch (error) {
        console.error('Error uploading file:', error);
        alert('Failed to upload file');
      } finally {
        setIsUploading(false);  // End uploading state
      }
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
      <h2>Sabancı University Document Management System</h2>

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
          <div className="file-upload-container">
            <label htmlFor="upload-file" className="upload-button">
              {isUploading ? 'Uploading...' : 'Upload PDF'}
            </label>
            <input
              type="file"
              id="upload-file"
              accept="application/pdf"
              onChange={handleFileUpload}
              style={{ display: 'none' }}  // Hide the default file input
            />
          </div>

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
     
        <div className={`nav-item ${selectedItem === "uploads" ? "selected" : ""}`} onClick={handleUploadsClick}>Documents</div>
        <div className={`nav-item ${selectedItem === "settings" ? "selected" : ""}`} onClick={handleSettingsClick}>Settings</div>
      </div>
    </div>
  );
};

export default SidePanel;
