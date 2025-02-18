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
documents_collection = db[DOCUMENTS_COLLECTION]

# Initialize GridFS
fs = GridFS(db)

# Function to add a document to MongoDB using GridFS
def add_document_to_mongo(file_data, filename, metadata=None):
    """
    Store a document in MongoDB (not using GridFS).
    """

    try:
        # Check if a document with the same filename exists
        if documents_collection.find_one({"filename": filename}):
            raise ValueError(f"A document with the filename '{filename}' already exists.")

        document = {
            "filename": filename,
            "file_data": file_data,  # Binary PDF data
            "metadata": metadata or {},
        }
        result = documents_collection.insert_one(document)
        return str(result.inserted_id)

    except ValueError as ve:
        print(f"Validation Error: {ve}")
        raise  # Re-raise the error so it can be handled by the caller
    except Exception as e:
        print(f"Error storing document in MongoDB: {e}")
        return None

# Function to list all documents with full details
def list_documents():
    
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
def get_document_by_id(document_id):
    """
    Retrieve a document from MongoDB by its ID.
    """
    try:
        print(f"Raw document_id: {document_id} (Type: {type(document_id)})")

        if isinstance(document_id, str):
            document_id = ObjectId(document_id)
        print(f"converted document_id: {document_id} (Type: {type(document_id)})")

        document = documents_collection.find_one({'_id': document_id})

        return document if document else None
    except Exception as e:
        print(f"Error retrieving document from MongoDB: {e}")
        return None

# Function to delete a document
def delete_document_from_mongo(id):
    try:
        if isinstance(id, str):
            id = ObjectId(id)
        
        # Remove reference from documents collection
        documents_collection.delete_one({"_id": id})
        
        print(f"Deleted document with ID: {id}")
    except Exception as e:
        print(f"Error deleting document: {e}")
        raise


def is_file_already_uploaded(filename):
    """Check if the file already exists in MongoDB."""

    return db['documents'].find_one({"filename": filename})


def get_file_by_highlighted_name(id):
    query = {"filename": {"$regex": f"^highlighted_{id}.*\.pdf$"}}
    return documents_collection.find(query)
