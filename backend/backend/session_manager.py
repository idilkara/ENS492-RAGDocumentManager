from pymongo import MongoClient
from datetime import datetime
from config import MONGO_URI, SESSIONS_COLLECTION, DB_NAME
import uuid
from bson import ObjectId

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
chats_collection = db[SESSIONS_COLLECTION]

def create_empty_session(user_id):
    """
    Create a new empty chat session for a user.
    """
    # Create MongoDB ObjectId for session_id directly
    session_id = ObjectId()
    
    # Check if a session with the same user_id and session_id already exists
    existing_session = chats_collection.find_one({"user_id": user_id, "session_id": session_id})
    while existing_session:
        print("Session already exists.")
        session_id = ObjectId()  # Generate a new ObjectId if it exists
        existing_session = chats_collection.find_one({"user_id": user_id, "session_id": session_id})
    
    # Create an empty chat session
    new_chat_session = {
        "user_id": user_id,
        "session_id": session_id,
        "conversation": [],  # Initialize as an empty list
        "created_at": datetime.utcnow()
    }
    
    # Insert into MongoDB
    chats_collection.insert_one(new_chat_session)
    print("New empty session created.")
    return {"message": "New empty session created.", "session_id": str(session_id)}

def add_message(user_id, session_id, user_query, agent_response, highlighted_pdf_path):
    """
    Add a new message to an existing chat session.
    If the session doesn't exist, create a new one with the message.
    """
    # Prepare the message structure
    new_message = {
        "user_query": user_query,
        "agent_response": agent_response,
        "highlighted_pdf": highlighted_pdf_path
    }
    
    # Check if a chat session already exists
    chat_session = chats_collection.find_one({"user_id": user_id, "session_id": session_id})
    if chat_session:
        # Append new message to the existing conversation
        chats_collection.update_one(
            {"_id": chat_session["_id"]},
            {"$push": {"conversation": new_message}}
        )
        print("Message appended to existing session.")
    else:
        # Create a new chat session with the message
        chat_document = {
            "user_id": user_id,
            "session_id": session_id,
            "conversation": [new_message],
            "created_at": datetime.utcnow()
        }
        chats_collection.insert_one(chat_document)
        print("New chat session created with the first message.")

def get_chat_session(user_id, session_id):
    """
    Retrieve a chat session by user_id and session_id.
    """
    chat_session = chats_collection.find_one({"user_id": user_id, "session_id": session_id})
    if chat_session:
        return chat_session["conversation"]
    else:
        print("Chat session not found.")
        return []

def get_session_list(user_id):
    """
    Retrieve session list for a user with ObjectIds converted to strings.
    """
    sessions = list(chats_collection.find({"user_id": user_id}))
    
    # Convert ObjectIds to strings
    for session in sessions:
        session['session_id'] = str(session['session_id'])
        session['_id'] = str(session['_id'])
        session["user_id"] = str(session["user_id"])
        session['created_at'] = session['created_at'].isoformat()
    
    #print("sessions: ", sessions)
    return sessions
