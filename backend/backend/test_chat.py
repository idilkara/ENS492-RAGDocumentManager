import requests

# Step 1: Login
login_url = "http://localhost:5000/login"
login_payload = {
    "email": "test@sabanciuniv.edu",
    "password": "securepassword"
}

login_response = requests.post(login_url, json=login_payload)
login_data = login_response.json()

if login_data.get("success"):
    token = login_data["token"]
    user_id = login_data["user_id"]
    print("Login successful.")
    print(f"Token: {token}")
    print(f"User ID: {user_id}")
else:
    print("Login failed:", login_data)
    exit()

# Step 2: Create Chat Session
session_url = "http://localhost:5000/create_chat_session"
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {token}"
}
session_payload = {
    "user_id": user_id
}

session_response = requests.post(session_url, headers=headers, json=session_payload)
session_data = session_response.json()

if session_response.ok:
    session_id = session_data["session_id"]
    print("Session created.")
    print(f"Session ID: {session_id}")
else:
    print("Failed to create session:", session_data)
    exit()

# Step 3: Send User Query
query_url = "http://localhost:5000/user_query"
query_payload = {
    "user_id": user_id,
    "session_id": session_id,
    "query": "What is the capital of France?",
    "model": "default_model",
    "language": "eng"
}

query_response = requests.post(query_url, headers=headers, json=query_payload)
query_data = query_response.json()

print("Query response:")
print(query_data)
