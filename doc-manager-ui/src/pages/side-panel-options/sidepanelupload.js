import React, { useState } from 'react';
import './sidepanelupload.css'; // Import the CSS file for styling
import config from "../../config";

const FileUpload = () => {
  const [uploadStatus, setUploadStatus] = useState(null); // State to track upload success or error
  const [isUploading, setIsUploading] = useState(false);

  const handleFileUpload = async (event) => {
    const files = event.target.files;
    console.log("Files selected:", files);

    if(files.length === 0) {
      setUploadStatus({success: false, message: 'No files selected.'});
      return;
    }

    const allowedTypes = ['application/pdf'];
    const invalidFiles = Array.from(files).filter(file => !allowedTypes.includes(file.type));

    if(invalidFiles.length > 0) {
      setUploadStatus({success: false, message: 'Please upload a valid PDF file.'});
      return;
    }

    try {
      setIsUploading(true); // Start uploading state
      console.log('Uploading started...');

      const formData = new FormData();
      for(let i = 0; i < files.length; i++) {
        formData.append('file', files[i]);
      }

      formData.append("replace_existing", "true");

      const token = localStorage.getItem("authToken");
      const response = await fetch(`${config.API_BASE_URL}/upload`, {
        method: 'POST',
        body: formData,
        headers: {'Authorization': `Bearer ${token}`}
      });

      const result = await response.json();
      console.log('Upload result:', result);

      if (response.ok) {
        if(result.warning) {
          setUploadStatus({ success: false, message: `Some files failed: ${result.failed_files.map(f => f.filename).join(", ")}`,});
        }
        else {
          setUploadStatus({ success: true, message: result.message });
        }
      } else if(response.status === 403) {
        setUploadStatus({ success: false, message: 'You need to be an admin to upload files'});
      } else {
        setUploadStatus({ success: false, message: result.error || 'Error uploading the file' });
      }
    } catch (error) {
      console.error('Error uploading file:', error);
      setUploadStatus({ success: false, message: 'Failed to upload file' });
    } finally {
      setIsUploading(false); // End uploading state
    }
  };

  return (
    <div className="file-upload-container">

      <label className="upload-button">
        {isUploading ? 'Uploading...' : 'Choose PDF'}
        <input type="file" multiple accept="application/pdf"  onChange={handleFileUpload} hidden />
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
