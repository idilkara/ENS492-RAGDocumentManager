import React, { useState, useEffect } from 'react';
import './documentManagement.css';
import { Eye, Trash2 } from 'lucide-react';
import config from "../config";

const DocumentManagement = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const [documents, setDocuments] = useState([]);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [documentToDelete, setDocumentToDelete] = useState(null);

  useEffect(() => {
    fetchDocuments();
  }, []);

  const fetchDocuments = async () => {
    try {
      const response = await fetch(`${config.API_BASE_URL}/get_documents`);
      const data = await response.json();

      if (response.ok) {
        setDocuments(data);
      } else {
        console.error('Error fetching documents:', data.error);
      }
    } catch (error) {
      console.error('Error fetching documents:', error);
    }
  };

  const viewDocument = async (e, docId) => {
    e.stopPropagation();
    try {
      const response = await fetch(`${config.API_BASE_URL}/get_pdf?file_id=${docId}`);
      if (response.ok) {
        const blob = await response.blob();
        const url = URL.createObjectURL(blob);
        window.open(url, '_blank');
      } else {
        console.error('Error fetching PDF:', await response.json());
      }
    } catch (error) {
      console.error('Error fetching PDF:', error);
    }
  };

  const openDeleteModal = (e, docId) => {
    e.stopPropagation();
    setDocumentToDelete(docId);
    setIsModalOpen(true);
  };

  const deleteDocument = async () => {
    if (!documentToDelete) return;

    try {
      const response = await fetch(`${config.API_BASE_URL}/delete_document?file_id=${documentToDelete}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
      });

      const data = await response.json();
      if (response.ok) {
        setDocuments(documents.filter(doc => doc.id !== documentToDelete));
        console.log('Document deleted:', data.message);
      } else {
        console.error('Error deleting document:', data.error);
      }
    } catch (error) {
      console.error('Error deleting document:', error);
    }

    setIsModalOpen(false);
    setDocumentToDelete(null);
  };

  const handleSearch = (e) => {
    setSearchTerm(e.target.value);
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
            onChange={handleSearch}
            className="search-input"
          />
          <button className="view-button" onClick={fetchDocuments}>REFRESH</button>
        </div>

        <div className="document-list">
          {filteredDocuments.length > 0 ? (
            filteredDocuments.map(doc => (
              <div key={doc.id} className="document-item">
                <span className="document-name">{doc.name}</span>
                <div className="document-buttons">
                  <button className="view-button" onClick={(e) => viewDocument(e, doc.id)}>
                    <Eye size={16} /> VIEW
                  </button>
                  <button className="delete-button" onClick={(e) => openDeleteModal(e, doc.id)}>
                    <Trash2 size={16} /> DELETE
                  </button>
                </div>
              </div>
            ))
          ) : (
            <div>No documents found</div>
          )}
        </div>
      </div>

      {isModalOpen && (
        <div className="modal-overlay">
          <div className="modal">
            <h3>Confirm Deletion</h3>
            <p>Are you sure you want to delete this document?</p>
            <div className="modal-buttons">
              <button className="confirm-button" onClick={deleteDocument}>Yes, Delete</button>
              <button className="cancel-button" onClick={() => setIsModalOpen(false)}>Cancel</button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default DocumentManagement;