# Document Management System Documentation (documents.py)

## Overview
The document management system handles the storage, retrieval, and management of documents in MongoDB, providing a robust interface for document operations in the RAG system.

## Database Configuration
```python
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
documents_collection = db[DOCUMENTS_COLLECTION]
fs = GridFS(db)
```

## Core Functions

### 1. Document Storage
#### `add_document_to_mongo(file_data, filename, metadata=None)`
- Stores documents in MongoDB collection
- Features:
  - Duplicate filename checking
  - Binary data storage
  - Metadata support
  - Error handling
- Returns:
  - Document ID (string) on success
  - None on failure

```python
document = {
    "filename": filename,
    "file_data": file_data,  # Binary PDF data
    "metadata": metadata or {},
}
```

### 2. Document Retrieval
#### `get_document_by_id(document_id)`
- Retrieves documents by their MongoDB ID
- Features:
  - ID type conversion (string to ObjectId)
  - Error handling
  - Null checking
- Returns:
  - Document object if found
  - None if not found or error occurs

### 3. Document Listing
#### `list_documents()`
- Lists all documents in the collection
- Features:
  - Full document details
  - GridFS file information
  - Pretty printing for debugging
- Returns:
  - List of all documents

### 4. Document Deletion
#### `delete_document_from_mongo(id)`
- Removes documents from MongoDB
- Features:
  - ID type conversion
  - Error handling
  - Cleanup of document references
- Returns:
  - None (raises exception on error)

### 5. File Existence Check
#### `is_file_already_uploaded(filename)`
- Checks for duplicate filenames
- Returns:
  - Document if found
  - None if not found

### 6. Highlighted File Retrieval
#### `get_file_by_highlighted_name(id)`
- Retrieves highlighted PDF files
- Uses regex pattern matching
- Returns:
  - Cursor of matching documents

## Error Handling
The system implements comprehensive error handling:
1. **Validation Errors**
   - Duplicate filename checking
   - Input validation
   - Type checking

2. **Database Errors**
   - Connection errors
   - Query errors
   - ID conversion errors

3. **File Operation Errors**
   - Binary data handling
   - File retrieval errors
   - GridFS operation errors

## Data Structure

### Document Schema
```python
{
    "_id": ObjectId,
    "filename": String,
    "file_data": Binary,
    "metadata": {
        # Optional metadata fields
    }
}
```

### GridFS Integration
- Used for large file storage
- Maintains file metadata
- Provides efficient file retrieval

## Best Practices

### 1. Document Storage
- Validate input data
- Check for duplicates
- Handle binary data properly
- Include metadata when available

### 2. Error Handling
- Use try-catch blocks
- Provide meaningful error messages
- Log errors for debugging
- Clean up resources on failure

### 3. ID Management
- Convert string IDs to ObjectId
- Validate ID format
- Handle invalid IDs gracefully

### 4. File Operations
- Check file existence
- Handle binary data safely
- Clean up temporary files
- Validate file types

## Dependencies
- pymongo
- gridfs
- fitz (PyMuPDF)
- bson

## Usage Examples

### Adding a Document
```python
file_data = # binary file data
filename = "example.pdf"
metadata = {"author": "John Doe"}
doc_id = add_document_to_mongo(file_data, filename, metadata)
```

### Retrieving a Document
```python
document = get_document_by_id("507f1f77bcf86cd799439011")
if document:
    # Process document
```

### Deleting a Document
```python
try:
    delete_document_from_mongo("507f1f77bcf86cd799439011")
except Exception as e:
    # Handle error
```

## Security Considerations
1. **Input Validation**
   - Validate filenames
   - Check file types
   - Sanitize metadata

2. **Access Control**
   - Implement proper authentication
   - Validate user permissions
   - Secure file operations

3. **Data Protection**
   - Handle sensitive data
   - Implement proper cleanup
   - Secure binary storage

## Performance Considerations
1. **Storage Optimization**
   - Use appropriate indexes
   - Implement efficient queries
   - Handle large files properly

2. **Query Optimization**
   - Use proper indexing
   - Implement efficient searches
   - Handle large result sets

3. **Resource Management**
   - Clean up temporary files
   - Handle memory efficiently
   - Manage database connections