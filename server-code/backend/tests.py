import requests
import json
import os

BASE_URL = "http://127.0.0.1:5000"


def test_upload(file_path, replace_existing=False):
    with open(file_path, "rb") as f:
        files = {"file": f}
        data = {"replace_existing": str(replace_existing).lower()}
        response = requests.post(f"{BASE_URL}/upload", files=files, data=data)
    print(response.json())


def test_delete(file_path):
    data = {"file_path": file_path}
    response = requests.post(f"{BASE_URL}/delete", json=data)
    print(response.json())


def test_get_pdf(file_path):
    response = requests.get(f"{BASE_URL}/get_pdf", params={"file_path": file_path})
    if response.status_code == 200:
        with open("downloaded.pdf", "wb") as f:
            f.write(response.content)
        print("PDF downloaded successfully.")
    else:
        print(response.json())


def test_user_query(user_id, session_id, query):
    data = {"user_id": user_id, "session_id": session_id, "query": query}
    response = requests.post(f"{BASE_URL}/user_query", json=data)
    print(f"Status Code: {response.status_code}")
    print(f"Raw Response: {response.text}")  # Print raw response before parsing JSON

    # Only parse JSON if the response is not empty
    if response.text.strip():
        print(response.json())
    else:
        print("❌ Error: Backend returned an empty response!")



def test_get_highlighted_pdf(gridfs_id):
    response = requests.get(f"{BASE_URL}/get_highlighted_pdf", params={"gridfs_id": gridfs_id})
    if response.status_code == 200:
        with open("highlighted.pdf", "wb") as f:
            f.write(response.content)
        print("Highlighted PDF downloaded successfully.")
    else:
        print(response.json())


def test_create_chat_session(user_id):
    data = {"user_id": user_id}
    response = requests.post(f"{BASE_URL}/create_chat_session", json=data)
    print(response.json())
    return response.json().get("session_id")


def test_get_chat_session(user_id, session_id):
    response = requests.get(f"{BASE_URL}/get_chat_session", params={"user_id": user_id, "session_id": session_id})
    print(response.json())


def test_get_user_sessions(user_id):
    response = requests.get(f"{BASE_URL}/get_user_sessions", params={"user_id": user_id})
    print(response.json())


if __name__ == "__main__":
    #test_upload("./upload/ECON_400_Lecture_Slides_1.pdf")  # Upload a sample PDF file
    #test_upload("sample.pdf")  # Delete the uploaded file
    #test_get_pdf("sample.pdf")  # Retrieve the uploaded file
    user_id = "user123"
    session_id = test_create_chat_session(user_id)  # Create a chat session
    if session_id:
        test_user_query(user_id, session_id, "who is the instrucor of DA510 Data Mining  course?")  # Test user query
    #test_get_user_sessions(user_id)  # Retrieve user sessions
