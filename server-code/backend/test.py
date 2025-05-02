from pymongo import MongoClient
from gridfs import GridFS
from config import MONGO_URI, DB_NAME, DOCUMENTS_COLLECTION
import traceback

client = MongoClient(MONGO_URI)
db = client[DB_NAME]

def test_mongodb_connection():
    try:
        # Establish connection
        client = MongoClient(MONGO_URI)
        
        # Test connection
        client.admin.command('ismaster')
        
        # Print database information
        print("Connected Databases:", client.list_database_names())
        
        # Select database
        db = client[DB_NAME]
        
        # Print collections
        print(f"Collections in {DB_NAME}:", db.list_collection_names())
        
        # Check documents collection
        documents_collection = db[DOCUMENTS_COLLECTION]
        print(f"Total documents in {DOCUMENTS_COLLECTION}: {documents_collection.count_documents({})}")
        
        # Check GridFS
        fs = GridFS(db)
        print("GridFS file count:", len(list(fs.find())))
        
    except Exception as e:
        print("MongoDB Connection Error:")
        print(traceback.format_exc())

def verify_documents():
    documents_collection = db[DOCUMENTS_COLLECTION]
    fs = GridFS(db)

    print("\n--- Document Verification ---")
    documents = list(documents_collection.find())
    
    for doc in documents:
        print("\nDocument:")
        print("Filename:", doc.get('filename'))
        print("GridFS ID:", doc.get('gridfs_id'))
        
        try:
            # Try to retrieve the file from GridFS
            gridfs_file = fs.get(doc['gridfs_id'])
            print("File Details:")
            print("  Filename:", gridfs_file.filename)
            print("  Size:", gridfs_file.length, "bytes")
        except Exception as e:
            print(f"Error retrieving file: {e}")

    return documents

import pprint
fs = GridFS(db)
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

list_documents()