# app.py
from flask import Flask, Response, request, jsonify
from flask_cors import CORS
import os
from flask import send_file
from vector_store import add_document, search_query, highlight_text_in_pdf
import uuid
from session_manager import create_empty_session, get_chat_session, get_session_list, chats_collection
import gridfs
from documents import get_document_by_id, delete_document_from_mongo
from io import BytesIO
from bson.objectid import ObjectId


app = Flask(__name__)
CORS(app)

# CAS Auth icin
# from flask_cas import CAS
# CAS(app)

# app.config['CAS_SERVER'] = 'https://sso.pdx.edu'
# app.config['CAS_AFTER_LOGIN'] = 'route_root'


#AAAAAAAAAAAAAAA
# ===============================
@app.route('/upload', methods=['POST'])
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
@app.route("/delete", methods=["POST"])
def delete_document_endpoint():
    """Endpoint to delete a document."""
    data = request.get_json()
    file_path = data.get("file_path")
    if not file_path:
        return jsonify({"error": "No file path provided"}), 400

    # Delete the document from the vector store and the file system
    delete_document_from_mongo(file_path)
    return jsonify({"message": f"File {file_path} has been deleted."}), 200

# ===============================
@app.route('/get_pdf', methods=['GET'])
def get_pdf():
    file_path = request.args.get('file_path')  # File path from the query string
    print("get_pdf file path: ", file_path)

    if not file_path or not os.path.exists(file_path):
        return jsonify({"error": "File not found"}), 404

    # Serve the file
    return send_file(file_path, as_attachment=True)

# ===============================
@app.route("/user_query", methods=["POST"])
def user_query():
    data = request.get_json()
    user_id = data.get("user_id")
    session_id = data.get("session_id")
    session_id = ObjectId(session_id)
    query = data.get("query")

    if not query or not user_id or not session_id:
        return jsonify({"error": "Missing required fields"}), 400

    response_text = search_query(query, user_id, session_id)
    highlighted_pdf_path = response_text.get("highlighted_pdf_path")

    print("ENDPOİNTTE GRIDFS:::::::::", response_text.get("gridfs"))

    return jsonify({
        "response": response_text.get("response"),
        "file_path": response_text.get("file_path"),
        "highlighted_pdf_path": highlighted_pdf_path,
        "gridfs": response_text.get("gridfs")
    })

# ===============================

@app.route('/get_highlighted_pdf', methods=['GET'])
def get_highlighted_pdf():
    gridfs_id = request.args.get('gridfs_id')  # GridFS ID from the query string
    gridfs_id = ObjectId(gridfs_id)

    print("get_highlighted_pdf GridFS ID: ", gridfs_id)


    if not gridfs_id:
        return jsonify({"error": "GridFS ID not provided"}), 400

    # Retrieve the file from GridFS
    pdf_file = get_document_by_id(gridfs_id)
    if pdf_file is None:
        return jsonify({"error": "File not found"}), 404

    # Serve the file
    return send_file(BytesIO(pdf_file.read()), as_attachment=True, download_name=pdf_file.filename)



# ===============================
# create new chat
@app.route("/create_chat_session", methods=["POST"])
def create_chat_session():
    """
    Create a new empty chat session for a user.
    """
    data = request.get_json()
    user_id = data.get("user_id")
    print("user id:", user_id)

    if not user_id:
        return jsonify({"error": "Missing user_id"}), 400

    result = create_empty_session(user_id)
    if "error" in result:
        return jsonify({"error": result["error"]}), 400

    return jsonify({"message": result["message"], "session_id": result["session_id"]}), 200


# ===============================
# Retrieve an existing chat session
@app.route("/get_chat_session", methods=["GET"])
def retrieve_chat_session():
    """
    Retrieve an existing chat session.
    """
    user_id = request.args.get("user_id")
    session_id = request.args.get("session_id")
    session_id = ObjectId(session_id)
    print("user id:", user_id)
    print("session id:", session_id)


    if not user_id or not session_id:
        return jsonify({"error": "Missing user_id or session_id"}), 400

    result = get_chat_session(user_id, session_id)
    if "error" in result:
        return jsonify({"error": result["error"]}), 404

    return jsonify(result), 200

# ===============================
# get all sessions of the user
@app.route('/get_user_sessions', methods=['GET'])
def get_user_sessions():
    """
    Retrieve all sessions for a given user, excluding the conversation.
    This returns session metadata for all sessions of a user.
    """
    user_id = request.args.get('user_id')
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
def delete_chat_session():
    """
    Delete a chat session by user_id and session_id.
    """
    data = request.get_json()
    user_id = data.get("user_id")
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
def delete_all_chat_sessions():
    """Deletes all chat sessions for a given user."""
    data = request.get_json()
    user_id = data.get("user_id")

    if not user_id:
        return jsonify({"error": "Missing user_id"}), 400

    try:
        # Delete all chat sessions for this user
        chats_collection.delete_many({"user_id": user_id})
        return jsonify({"message": "All chat sessions deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500



if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
