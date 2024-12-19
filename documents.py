#documents.py
from pymongo import MongoClient
from gridfs import GridFS
from config import MONGO_URI, DB_NAME, DOCUMENTS_COLLECTION
import traceback
import datetime
import os
import pprint
from io import BytesIO
import fitz
from bson import ObjectId

# Create MongoDB client and database
client = MongoClient(MONGO_URI)
db = client[DB_NAME]

# Initialize GridFS
fs = GridFS(db)

# Function to add a document to MongoDB using GridFS
def add_document_to_mongo(file_path, metadata):
    try:
        # Enhanced logging
        print("=" * 50)
        print("Attempting to store document:")
        print("File Path:", file_path)
        print("Metadata:")
        pprint.pprint(metadata)
        
        # Detailed file checks
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File does not exist: {file_path}")
        
        file_size = os.path.getsize(file_path)
        print(f"File Size: {file_size} bytes")
        
        # Open and store file
        with open(file_path, 'rb') as file_data:
            file_id = fs.put(
                file_data, 
                filename=metadata.get('file_name', 'unknown'),
                content_type='application/pdf',  # Add content type
                metadata=metadata,
                upload_date=datetime.datetime.utcnow()
            )
        
        # Verify file was stored in GridFS
        stored_file = fs.get(file_id)
        print("GridFS File Details:")
        print("File ID:", file_id)
        print("Filename:", stored_file.filename)
        print("Length:", stored_file.length)
        
        # Store reference in documents collection
        documents_collection = db[DOCUMENTS_COLLECTION]
        document_ref = {
            "gridfs_id": file_id,
            "filename": metadata.get('file_name', 'unknown'),
            "metadata": metadata,
            "uploaded_at": datetime.datetime.utcnow(),
            "file_size": file_size
        }
        
        # Insert and verify
        insert_result = documents_collection.insert_one(document_ref)
        print("Document Reference:")
        pprint.pprint(document_ref)
        print("Inserted Document ID:", insert_result.inserted_id)
        
        print("=" * 50)
        return file_id
    
    except Exception as e:
        print("DETAILED ERROR:")
        print(traceback.format_exc())
        raise

# Function to list all documents with full details
def list_documents():
    documents_collection = db[DOCUMENTS_COLLECTION]
    
    # Retrieve all document references with full details
    documents = list(documents_collection.find())
    
    # Print documents with full details
    print("\n--- All Stored Documents ---")
    for doc in documents:
        print("\nDocument:")
        pprint.pprint(doc)
        
        # Try to retrieve the GridFS file
        try:
            gridfs_file = fs.get(doc['gridfs_id'])
            print("GridFS File Details:")
            print("Filename:", gridfs_file.filename)
            print("Length:", gridfs_file.length)
        except Exception as e:
            print(f"Error retrieving GridFS file: {e}")
    
    return documents

# Function to retrieve a file from GridFS
def get_document_by_id(gridfs_id):
    try:
        # Retrieve file from GridFS
        file = fs.get(gridfs_id)
        print(file)
        return file
    except Exception as e:
        print(f"Error retrieving file: {e}")
        return None

# Function to delete a document
def delete_document_from_mongo(gridfs_id):
    try:
        # Delete file from GridFS
        fs.delete(gridfs_id)
        
        # Remove reference from documents collection
        documents_collection = db[DOCUMENTS_COLLECTION]
        documents_collection.delete_one({"gridfs_id": gridfs_id})
        
        print(f"Deleted document with GridFS ID: {gridfs_id}")
    except Exception as e:
        print(f"Error deleting document: {e}")
        raise


def is_file_already_uploaded(filename):
    """Check if the file already exists in MongoDB."""

    return db['fs.files'].find_one({"filename": filename})


def get_file_by_highlighted_name(id):
    documents_collection = db[DOCUMENTS_COLLECTION]
    query = {"filename": {"$regex": f"^highlighted_{id}.*\.pdf$"}}
    return documents_collection.find(query)
