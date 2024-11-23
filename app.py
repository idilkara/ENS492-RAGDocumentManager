# app.py
from flask import Flask, Response, request, jsonify
from flask_cors import CORS
import os
from vector_store import add_document, list_documents, search_query, UPLOAD_FOLDER

app = Flask(__name__)
CORS(app)

# CAS Auth icin
# from flask_cas import CAS
# CAS(app)

# app.config['CAS_SERVER'] = 'https://sso.pdx.edu'
# app.config['CAS_AFTER_LOGIN'] = 'route_root'

#AAAAAAAAAAAAAAA
@app.route("/upload", methods=["POST"])
def upload_document():
    """Endpoint to upload a document."""
    if "file" not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No file selected for uploading"}), 400

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)
    
    # Add document to vector store
    add_document(file_path)
    return jsonify({"message": f"File {file.filename} has been uploaded and processed."}), 200

@app.route("/documents", methods=["GET"])
def get_documents():
    """Endpoint to retrieve all uploaded documents."""
    documents = list_documents()
    return jsonify({"documents": documents})

# @app.route("/user_query", methods=["POST"])
# def user_query():
#     """Endpoint to receive a query from the user and return a response."""
#     data = request.get_json()
#     user_query = data.get("query")
    
#     if not user_query:
#         return jsonify({"error": "No query provided"}), 400
    
#     # Call the vector store's search function
#     response = search_query(user_query)
#     return jsonify({"response": response})

@app.route("/user_query", methods=["POST"])
def user_query():
    data = request.get_json()
    query = data.get("query")
    if not query:
        return jsonify({"error": "No query provided"}), 400

    def generate_response():
        for chunk in search_query(query):  # Replace with your LLM/embedding retrieval
            yield chunk  # Send each chunk progressively

    return Response(generate_response(), content_type="application/json")

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
