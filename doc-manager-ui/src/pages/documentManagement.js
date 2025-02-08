import React, { useState, useEffect } from 'react';
import './documentManagement.css';
import config from "../config";


const DocumentManagement = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const [documents, setDocuments] = useState([]);
  const [selectedDocument, setSelectedDocument] = useState(null);

  useEffect(() => {
    fetchDocuments();
  }, []);

  const fetchDocuments = async () => {
    try {
      // Make an API call to fetch the documents from the backend
      const response = await fetch(`${config.API_BASE_URL}/get_documents`);  // Replace with your backend URL
      const data = await response.json();

      if (response.ok) {
        setDocuments(data);  // Set the documents from the database into the state
      } else {
        console.error('Error fetching documents:', data.error);
      }
    } catch (error) {
      console.error('Error fetching documents:', error);
    }
  };

  const viewDocument = async () => {
    if (!selectedDocument) {
      console.error('No document selected!');
      return;
    }
  
    try {
      // Fetch the PDF using the selected document ID
      const response = await fetch(`${config.API_BASE_URL}/get_pdf?file_id=${selectedDocument}`);
      if (response.ok) {
        const blob = await response.blob();  // Convert the response to a Blob (binary data)
        const url = URL.createObjectURL(blob);  // Create a URL for the Blob object
        window.open(url, '_blank');  // Open the PDF in a new tab
      } else {
        console.error('Error fetching PDF:', await response.json());
      }
    } catch (error) {
      console.error('Error fetching PDF:', error);
    }
  };

  const deleteDocument = async () => {
    if (!selectedDocument) {
      console.error('No document selected!');
      return;
    }
  
    try {
      // Send request to delete the document
      const response = await fetch(`${config.API_BASE_URL}/delete_document?file_id=${selectedDocument}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
      });
  
      const data = await response.json();
  
      if (response.ok) {
        // On success, remove the deleted document from the list
        const updatedDocuments = documents.filter(doc => doc.id !== selectedDocument);
        setDocuments(updatedDocuments);
        setSelectedDocument(null); // Clear the selection
        console.log('Document deleted:', data.message);
      } else {
        console.error('Error deleting document:', data.error);
      }
    } catch (error) {
      console.error('Error deleting document:', error);
    }
  };
  

 

  const handleSearch = (e) => {
    setSearchTerm(e.target.value);
  };

  const handleSelectDocument = (doc) => {
    setSelectedDocument(doc.id);
  };

  

  const filteredDocuments = documents.filter(doc =>
    doc.name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  

  return (
    <div className="document-management-container">
      <div className="documents-container">
        <div className="input-container">
          <input
            type="text"
            placeholder="Search documents..."
            value={searchTerm}
            onChange={handleSearch}  // Handle user input for search
            className="search-input"
          />

          <button className="view-button" onClick={fetchDocuments}>
            REFRESH
          </button>

          <button
          className="view-button"
          onClick={viewDocument}  // Call the viewDocument function when clicking "VIEW"
          disabled={!selectedDocument}  // Disable button if no document is selected
        >  
 VIEW
 </button>
 <button
          className="view-button"
          onClick={deleteDocument}  // Call the deleteDocument function when clicking "DELETE"
          disabled={!selectedDocument}  // Disable button if no document is selected
        >
            DELETE
          </button>
        </div>

        <div className="document-list">
          {filteredDocuments.length > 0 ? (
            filteredDocuments.map(doc => (
              <div
                key={doc.id}
                className={`document-item ${selectedDocument === doc.id ? 'selected' : ''}`}
                onClick={() => handleSelectDocument(doc)}
              >
                {doc.name}
              </div>
            ))
          ) : (
            <div>No documents found</div>
          )}
        </div>
      </div>
    </div>
  );
};

export default DocumentManagement;