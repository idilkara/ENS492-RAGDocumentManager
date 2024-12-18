#history_manage.py
from pymongo import MongoClient
from config import MONGO_URI, DB_NAME, SESSIONS_COLLECTION

client = MongoClient(MONGO_URI)
db = client[DB_NAME]

# Function to add a chat history (user and session-based)
def add_to_history(user_id, session_id, user_query, agent_response):
    session_data = {
        "user_id": user_id,
        "session_id": session_id,
        "user_query": user_query,
        "agent_response": agent_response,
    }
    
    session_collection = db[SESSIONS_COLLECTION]
    
    # Ensure only last 2 queries and answers are stored for each session
    session_count = session_collection.count_documents({"user_id": user_id, "session_id": session_id})
    
    # if session_count >= 2:
    #     # Remove the oldest history entry for that session
    #     session_collection.delete_one({"user_id": user_id, "session_id": session_id})
    
    session_collection.insert_one(session_data)

# Function to get the last 2 chats for a session
def get_history(user_id, session_id):
    session_collection = db[SESSIONS_COLLECTION]
    # Fetch the history for the given user_id and session_id
    session_history = session_collection.find(
        {"user_id": user_id, "session_id": session_id},
        {"_id": 0, "user_query": 1, "agent_response": 1}
    ).sort("_id", -1).limit(2)
    
    # Return the history as a list of dictionaries
    return list(session_history)