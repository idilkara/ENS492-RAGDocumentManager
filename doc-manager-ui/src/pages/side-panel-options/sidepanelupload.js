import React, { useState } from 'react';
import './sidepanelupload.css'; // Import the CSS file for styling

const FileUpload = () => {
  const [uploadStatus, setUploadStatus] = useState(null); // State to track upload success or error
  const [isUploading, setIsUploading] = useState(false);

  const handleFileUpload = async (event) => {
    const file = event.target.files[0];
    console.log("File selected:", file);

    if (file && file.type === 'application/pdf') {
      try {
        setIsUploading(true); // Start uploading state
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
          setUploadStatus({ success: true, message: result.message });
        } else {
          setUploadStatus({ success: false, message: result.error || 'Error uploading the file' });
        }
      } catch (error) {
        console.error('Error uploading file:', error);
        setUploadStatus({ success: false, message: 'Failed to upload file' });
      } finally {
        setIsUploading(false); // End uploading state
      }
    } else {
      setUploadStatus({ success: false, message: 'Please upload a valid PDF file.' });
    }
  };

  return (
    <div className="file-upload-container">

      <label className="upload-button">
        {isUploading ? 'Uploading...' : 'Choose PDF'}
        <input type="file" accept="application/pdf" onChange={handleFileUpload} hidden />
      </label>

      {/* Feedback message */}
      {uploadStatus && (
        <div
          className={`upload-feedback ${uploadStatus.success ? 'success' : 'error'}`}
        >
          {uploadStatus.message}
        </div>
      )}
    </div>
  );
};

export default FileUpload;
