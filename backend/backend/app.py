# app.py
from flask import Flask, Response, request, jsonify
from flask_cors import CORS
import os
from flask import send_file
from vector_store import add_document, search_query, highlight_text_in_pdf
from session_manager import create_empty_session, get_chat_session, get_session_list
from documents import get_document_by_id, delete_document_from_mongo
from io import BytesIO
from bson.objectid import ObjectId
from config import EMBEDDING_MODEL_URL
from langchain_ollama import ChatOllama

app = Flask(__name__)

app.config['PROPAGATE_EXCEPTIONS'] = True  # ✅ Force full error messages
app.config['DEBUG'] = True  # ✅ Ensure debug mode is enabled





# @app.after_request
# def add_cors_headers(response):
#     """Ensure CORS headers are present in all responses"""
#     response.headers["Access-Control-Allow-Origin"] = request.headers.get("Origin", "*")
#     response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS, DELETE, PUT"
#     response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
#     response.headers["Access-Control-Allow-Credentials"] = "true"
#     return response


# # ✅ Explicitly handle `OPTIONS` preflight requests
# @app.route('/<path:path>', methods=['OPTIONS'])
# def handle_options(path):
#     response = jsonify({"message": "Preflight OK"})
#     response.headers["Access-Control-Allow-Origin"] = "http://localhost:3000"
#     response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS, DELETE, PUT"
#     response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
#     response.headers["Access-Control-Allow-Credentials"] = "true"
#     return response, 200

# CAS Auth icin
# from flask_cas import CAS
# CAS(app)

# app.config['CAS_SERVER'] = 'https://sso.pdx.edu'
# app.config['CAS_AFTER_LOGIN'] = 'route_root'


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

from flask import Flask, request, jsonify
from bson.objectid import ObjectId, InvalidId
import traceback

app = Flask(__name__)

@app.route("/user_query", methods=["POST"])
def user_query():
    try:
        data = request.get_json()
        user_id = data.get("user_id")
        session_id = data.get("session_id")
        query = data.get("query")

        print(f"🔍 Received user_query: user_id={user_id}, session_id={session_id}, query='{query}'")

        if not query or not user_id or not session_id:
            print("❌ ERROR: Missing required fields")
            return jsonify({"error": "Missing required fields"}), 400

        # ✅ Validate session_id format before converting to ObjectId
        try:
            session_id = ObjectId(session_id)
        except InvalidId:
            print(f"❌ ERROR: Invalid session_id format: {session_id}")
            return jsonify({"error": "Invalid session_id format"}), 400

        print("🔍 Calling search_query() with:", query, user_id, session_id)
        response_text = search_query(query, user_id, session_id)

        print(f"✅ Response from search_query: {response_text}")

        return jsonify({
            "response": response_text.get("response"),
            "file_path": response_text.get("file_path"),
            "highlighted_pdf_path": response_text.get("highlighted_pdf_path"),
            "gridfs": response_text.get("gridfs")
        })

    except Exception as e:
        print(f"❌ ERROR in /user_query: {e}")
        traceback.print_exc()  # ✅ Prints the full error
        return jsonify({"error": str(e)}), 500


    except Exception as e:
        print(f"❌ ERROR in /user_query: {e}")
        traceback.print_exc()  # ✅ Print the full error traceback
        return jsonify({"error": str(e)}), 500

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
def create_chat():
    return {"message": "Chat session created"}, 200


# @app.route("/create_chat_session", methods=["POST", "OPTIONS"])
# def create_chat_session():
#     """ Create a new chat session """

#     # ✅ Handle preflight request
#     if request.method == "OPTIONS":
#         response = jsonify({"message": "Preflight OK"})
#         response.headers["Access-Control-Allow-Origin"] = "http://localhost:3000"
#         response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
#         response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
#         return response, 200

#     # ✅ Handle normal POST request
#     data = request.get_json()
#     user_id = data.get("user_id")

#     if not user_id:
#         return jsonify({"error": "Missing user_id"}), 400

#     result = create_empty_session(user_id)
#     if "error" in result:
#         return jsonify({"error": result["error"]}), 400

#     return jsonify({"message": result["message"], "session_id": result["session_id"]}), 200


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


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
    print("🔄 Preloading LLM Model...")
    llm = ChatOllama(model="mistral:latest", base_url= EMBEDDING_MODEL_URL )
    print("✅ LLM Model Preloaded!")
