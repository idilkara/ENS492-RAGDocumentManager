import React, { useState, useEffect } from 'react';
import './documentManagement.css';
import { Eye, RefreshCcw, RefreshCwIcon, Trash2 } from 'lucide-react';
import config from "../config";
import apiFetch from '../api';

const DocumentManagement = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const [documents, setDocuments] = useState([]);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [documentToDelete, setDocumentToDelete] = useState(null);

/* The `useEffect` hook in React is used to perform side effects in function components. In this case,
the `useEffect` hook is being used to fetch documents when the component mounts for the first time. */
  useEffect(() => {
    fetchDocuments();
  }, []);

  const fetchDocuments = async () => {
    try {
      const data = await apiFetch(`${config.API_BASE_URL}/get_documents`);
      setDocuments(data);

    } catch (error) {
      console.error('Error fetching documents:', error);
    }
  };

  const viewDocument = async (e, docId) => {
    const token = localStorage.getItem("authToken");
    e.stopPropagation();
    try {
      const response = await fetch(`${config.API_BASE_URL}/get_pdf?file_id=${docId}`, {headers: {'Authorization': `Bearer ${token}`}});
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
    const token = localStorage.getItem("authToken");
    try {
      const response = await fetch(`${config.API_BASE_URL}/delete_document?file_id=${documentToDelete}`, {
        method: 'POST', 
        headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` },
      });

      const data = await response.json();
      if (response.ok) {
        setDocuments(documents.filter(doc => doc.id !== documentToDelete));
        console.log('Document deleted:', data.message);
      } else if(response.status === 403) {
        alert("You need to be an admin to delete a document!"); // placeholder admin degilsin alarmi
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
          <button className="view-button" onClick={fetchDocuments}>
            <RefreshCcw size={16} /> REFRESH
          </button>
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