# app.py
from flask import Flask, Response, request, jsonify, session
from flask_cors import CORS
import os
from flask import send_file
from vector_store import add_document, search_query, delete_document_vectorstore
import uuid
from session_manager import create_empty_session, get_chat_session, get_session_list, chats_collection
from documents import get_document_by_id, delete_document_from_mongo, documents_collection
from io import BytesIO
from bson.objectid import ObjectId
from config import MONGO_URI, DB_NAME, USERS_COLLECTION
import re
import jwt
from datetime import datetime, timedelta
from dotenv import load_dotenv
from functools import wraps
from pymongo import MongoClient


app = Flask(__name__)
CORS(app, origins=["http://localhost:3000"])

# CAS Auth icin
# from flask_cas import CAS
# CAS(app)

# app.config['CAS_SERVER'] = 'https://sso.pdx.edu'
# app.config['CAS_AFTER_LOGIN'] = 'route_root'

# login implementation requirements
EMAIL_REGEX = r'^[a-zA-Z0-9._%+-]+@sabanciuniv\.edu$'
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALLOWED_ROUTES = ['/login', '/logout']

client = MongoClient(MONGO_URI)
db = client[DB_NAME]  # Replace with your actual database name
users_collection = db[USERS_COLLECTION]

def get_user_by_email(email):
    return users_collection.find_one({"email": email})

# login api
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get("email", "").strip()
    password = data.get("password", "").strip()  # ignored for now

    if not re.match(EMAIL_REGEX, email):
        return jsonify({"success": False, "message": "Invalid university email!"}), 400

    # Find user by email
    user = get_user_by_email(email)

    if not user:
        return jsonify({"success": False, "message": "User not found. Please contact administrator."}), 401
    
    # Check password (assuming passwords are stored as plain text for now)
    # In production, you should use password hashing
    if user["password"] != password:
        return jsonify({"success": False, "message": "Invalid password"}), 401


    role = user["role"]
    user_id = user["_id"]
    user_id = str(user_id)

    expiration = datetime.now() + timedelta(minutes=60)
    token = jwt.encode({"email": email, "role": role, "exp": expiration}, SECRET_KEY, algorithm="HS256")

    return jsonify({"success": True, "message": "Login successful", "token": token, "role": role, "user_id": user_id})



@app.route('/register', methods=['POST'])
def register():
    # Get JSON data from request
    data = request.get_json()
    email = data.get("email", "").strip()
    password = data.get("password", "").strip()
    
    # Validate email format (must be a Sabancı University email)
    if not re.match(EMAIL_REGEX, email):
        return jsonify({
            "success": False, 
            "message": "Invalid university email! Please use your @sabanciuniv.edu email."
        }), 400
    
    # Check if user already exists
    existing_user = get_user_by_email(email)
    if existing_user:
        return jsonify({
            "success": False, 
            "message": "An account with this email already exists."
        }), 409
    
    # Validate password (you can add more complex validation as needed)
    if len(password) < 8:
        return jsonify({
            "success": False, 
            "message": "Password must be at least 8 characters long."
        }), 400
    
    # Create new user
    # In production, you should hash the password
    new_user = {
        "email": email,
        "password": password,  # In production, use password hashing
        "role": "student",  # Default role for new users
        "created_at": datetime.now()
    }
    
    try:
        # Insert the new user into the database
        result = users_collection.insert_one(new_user)
        
        if result.inserted_id:
            return jsonify({
                "success": True,
                "message": "Registration successful. You can now log in."
            }), 201
        else:
            return jsonify({
                "success": False, 
                "message": "Failed to create user. Please try again."
            }), 500
            
    except Exception as e:
        print(f"Registration error: {str(e)}")
        return jsonify({
            "success": False, 
            "message": "An error occurred during registration."
        }), 500

# middleware for authentication and role verification
@app.before_request
def check_token():
    print(SECRET_KEY)
    
    # Skip verification if the route is allowed or if the request is for registration
    if request.path in ALLOWED_ROUTES or request.method == "OPTIONS" or request.path == "/register":
        return
    
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        return jsonify({"success": False, "message": "Missing token"}), 401
    
    try:
        token = auth_header.split(" ")[1]
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        request.user_email = payload.get("email")
        request.user_role = payload.get("role")
    except jwt.ExpiredSignatureError:
        return jsonify({"success": False, "message": "Token expired"}), 401
    except jwt.InvalidSignatureError:
        return jsonify({"success": False, "message": "Invalid token"}), 401

    
# decorator to dedicate endpoints to admins only
def role_required(required_role):
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if getattr(request, "user_role", None) != required_role:
                return jsonify({"success": False, "message": "Access denied"}), 403
            return f(*args, **kwargs)
        return wrapped
    return decorator


#AAAAAAAAAAAAAAA
# ===============================
@app.route('/upload', methods=['POST'])             # Receives & reads file (sidepanelupload.js / handleFileUpload())
@role_required("admin") # only admins are allowed to upload
def upload():                                        
    file = request.files['file']
    replace_existing = request.form.get('replace_existing', 'false').lower() == 'true'          

    if not file:
        return jsonify({"error": "No file uploaded"}), 400

    file_entry = {
        "file_data": file.read(),
        "filename": file.filename
    }

    result = add_document(file_entry, replace_existing=replace_existing)
    
    if "error" in result:
        return jsonify({"error": result["error"]}), 500
    elif "warning" in result:
        return jsonify({
            "warning": result["warning"],
            "options": "Set 'replace_existing' to True to replace the file."
        }), 200
    else:
        return jsonify({"message": result["message"]}), 200


# ===============================
#delete document
@app.route("/delete_document", methods=["POST"])                       #is it currently used??
@role_required("admin")
def delete_document_endpoint():                                     # Gets file id and deletes from mongo and vector store, 
    """Endpoint to delete a document."""
    print("delete endpoint")
    file_id = request.args.get('file_id')
    print(file_id)
    if not file_id:
        return jsonify({"error": "No file id provided"}), 400

    # Delete the document from the vector store and the file system
    delete_document_from_mongo(file_id)
    delete_document_vectorstore(file_id)
    
    return jsonify({"message": f"File {file_id} has been deleted."}), 200

# ===============================
@app.route('/get_documents', methods=['GET'])
def get_documents():                                                # Retrives all documents stored in mongo as a list of doc ids and file names
    try:                                                                    # documentManagement.js / fetchDocuments
        # Fetch all documents from MongoDB
        documents = list(documents_collection.find())
        
        # Prepare the documents list for the frontend (you can modify it to send only necessary fields)
        result = [{'id': str(doc['_id']), 'name': doc['filename']} for doc in documents]
        
        return jsonify(result)
    except Exception as e:
        print(f"Error fetching documents: {e}")
        return jsonify({"error": "Failed to fetch documents"}), 500

# endpoint to return the desired pdf
@app.route('/get_pdf', methods=['GET'])
def get_pdf():                                                  #Retrieves a file, (documentManagement.js / viewDocuments())
    file_id = request.args.get('file_id')  
    print("get_pdf file id: ", file_id)

    file = get_document_by_id(file_id)
    if not file_id or not file:
        return jsonify({"error": "File not found"}), 404

    # Serve the file
    
    pdf_data = file.get("file_data")

    return send_file(BytesIO(pdf_data), as_attachment=True, download_name=file.get("filename"), mimetype="application/pdf")

# ===============================
@app.route("/user_query", methods=["POST"])
def user_query():                                               # chatbot.js / handleSendMessage()
    data = request.get_json()
    user_id = data.get("user_id")
    user_id = ObjectId(user_id)
    session_id = data.get("session_id")
    session_id = ObjectId(session_id)
    query = data.get("query")
    model = data.get("model")
    language = data.get("language", "eng")


    if not query or not user_id or not session_id:
        return jsonify({"error": "Missing required fields"}), 400

    response_text = search_query(query, user_id, session_id, model, language)
    source_docs_arr = response_text.get("source_docs_arr")

    print("ENDPOINTTE SOURCE_DOCS_ARR:::::::::", source_docs_arr, "\n", len(source_docs_arr))

    return jsonify({
        "response": response_text.get("response"),
        "file_path": response_text.get("file_path"),
        "source_docs_arr": source_docs_arr,
    })

# ===============================

@app.route('/get_highlighted_pdf', methods=['GET'])                         # chatbot.js / handleViewPDFClick()
def get_highlighted_pdf():
    pdf_path = request.args.get('file_path')
    print("istenilen path: ", pdf_path)
    if not pdf_path or not os.path.exists(pdf_path):
        return jsonify({"error": "File not found or expired"}), 404
    try:
        return send_file(
            pdf_path,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=f"highlighted_{os.path.basename(pdf_path)}"
        )
    except Exception as e:
        return jsonify({"error": f"Error serving file: {str(e)}"}), 500




# ===============================
# create new chat
@app.route("/create_chat_session", methods=["POST"])                            # main.js / createNewChatSession()
def create_chat_session():
    """
    Create a new empty chat session for a user.
    """
    data = request.get_json()
    user_id = data.get("user_id")
    user_id = ObjectId(user_id)
    print("user id:", user_id)

    if not user_id:
        return jsonify({"error": "Missing user_id"}), 400

    result = create_empty_session(user_id)
    if "error" in result:
        return jsonify({"error": result["error"]}), 400

    return jsonify({"message": result["message"], "session_id": result["session_id"]}), 200


# ===============================
# Retrieve an existing chat session

@app.route("/get_chat_session", methods=["GET"])                                  # main.js / getChatSession()
def retrieve_chat_session():
    
    #Retrieve an existing chat session.
    
    user_id = request.args.get("user_id")
    user_id = ObjectId(user_id)
    session_id = request.args.get("session_id")
    session_id = ObjectId(session_id)
    print("user id:", user_id)
    print("session id:", session_id)


    if not user_id or not session_id:
        return jsonify({"error": "Missing user_id or session_id"}), 400

    result = get_chat_session(user_id, session_id)
    print("SESSION RESULT::", result)
    if "error" in result:
        return jsonify({"error": result["error"]}), 404

    return jsonify(result), 200



# ===============================
# get all sessions of the user
@app.route('/get_user_sessions', methods=['GET'])                               # main.js / fetchUserSessions()
def get_user_sessions():
    """
    Retrieve all sessions for a given user, excluding the conversation.
    This returns session metadata for all sessions of a user.
    """
    user_id = request.args.get('user_id')
    user_id = ObjectId(user_id)
    print("user id:", user_id)

    if not user_id:
        return jsonify({"error": "user_id is required"}), 400

    # Query MongoDB for sessions associated with the user
    sessions = get_session_list(user_id)

    # if sessions.count() == 0:
    #     return jsonify({"error": "No sessions found for the given user_id"}), 404

    # Prepare a list of session metadata (without conversation)
    session_list = []  # Create a list to hold all sessions

    for session in sessions:
        # Check if the session has any conversations
        if session.get("conversation") and len(session["conversation"]) > 0:
            session_data = {
                "user_id": session["user_id"],
                "session_id": session["session_id"],
                "created_at": session["created_at"],
                "name": session["conversation"][0]["user_query"]
            }
        else:
            session_data = {
                "user_id": session["user_id"],
                "session_id": session["session_id"],
                "created_at": session["created_at"],
                "name": "Empty Chat"
            }
        session_list.append(session_data)  # Add each session to the list


    return jsonify(session_list)

@app.route("/delete_chat_session", methods=["POST"])
def delete_chat_session():                                                      # sidepanel.js / handleDeleteSession()
    """
    Delete a chat session by user_id and session_id.
    """
    data = request.get_json()
    user_id = data.get("user_id")
    user_id = ObjectId(user_id)
    session_id = data.get("session_id")

    if not user_id or not session_id:
        return jsonify({"error": "Missing user_id or session_id"}), 400

    try:
        session_id = ObjectId(session_id)
    except:
        return jsonify({"error": "Invalid session_id"}), 400

    # Delete session from MongoDB
    result = chats_collection.delete_one({"user_id": user_id, "session_id": session_id})

    if result.deleted_count == 0:
        return jsonify({"error": "Chat session not found"}), 404

    return jsonify({"message": "Chat session deleted successfully"}), 200

@app.route("/delete_all_chat_sessions", methods=["POST"])
def delete_all_chat_sessions():                                                     # sidepanel.js / handleClearAllSessions()
    """Deletes all chat sessions for a given user."""
    data = request.get_json()
    user_id = data.get("user_id")
    user_id = ObjectId(user_id)

    if not user_id:
        return jsonify({"error": "Missing user_id"}), 400

    try:
        # Delete all chat sessions for this user
        chats_collection.delete_many({"user_id": user_id})
        return jsonify({"message": "All chat sessions deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


#mock users (will be deleted later)
def insert_mock_users():
    """
    Insert mock users into the database if they don't already exist.
    This is for development/testing purposes only.
    """
    mock_users = [
        {
            "email": "admin@sabanciuniv.edu",
            "password": "admin",  # In production, use hashed passwords
            "role": "admin",
            "created_at": datetime.now()
        },
        {
            "email": "user@sabanciuniv.edu",
            "password": "user1",  # In production, use hashed passwords
            "role": "user",
            "created_at": datetime.now()
        },
        {
            "email": "user_iki@sabanciuniv.edu",
            "password": "user2",  # In production, use hashed passwords
            "role": "user",
            "created_at": datetime.now()
        }
    ]
    
    for user in mock_users:
        # Check if user already exists
        existing_user = users_collection.find_one({"email": user["email"]})
        if not existing_user:
            users_collection.insert_one(user)
            print(f"Mock user created: {user['email']} with role {user['role']}")


if __name__ == "__main__":
    insert_mock_users()
    app.run(debug=True, use_reloader=False, host="127.0.0.1", port=5000)        #use_reloader'ı vector store'a file yüklerken sürekli
                                                                                # Detected change in 'C:\\Program Files\\Python38\\Lib\\encodings\\cp1252.py', reloading
                                                                                # benzeri hatalar aldığım ve yüklemeyi kesintiye uğrattığı için kapattım.
                                                                                #Sorun çıkarırsa parametreyi kaldırabilirsiniz
