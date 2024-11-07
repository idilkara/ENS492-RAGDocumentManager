import os
import requests  # For making requests to Ollama API
import streamlit as st
from langchain.vectorstores import Chroma
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.chains import RetrievalQA

# Used to create the memory
from langchain.memory import ConversationBufferMemory
memory_key = "history"

# Ollama API endpoint
OLLAMA_API_URL = "http://localhost:11434"  # Ollama’s default local port

# Vector Database 
chromadb = "db"
upload_folder = "upload"
os.makedirs(upload_folder, exist_ok=True)
embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
vectorstore = Chroma(persist_directory=chromadb, embedding_function=embeddings)

# Define function to send a query to the Ollama model
def query_ollama(model, prompt):
    url = f"{OLLAMA_API_URL}/generate"
    headers = {
        "Content-Type": "application/json",
    }
    payload = {
        "model": model,
        "prompt": prompt,
    }
    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    return response.json()["response"]

# Streamlit UI
st.header("AI Assistant")
query = st.text_input("Enter your query")

if st.button("Retrieve"):
    # Set your desired model for Ollama
    model_name = "llama3.2:3b"  # Replace with the model available in Ollama

    # Retrieve answer from vector database
    qa = RetrievalQA.from_llm(query_ollama, retriever=vectorstore.as_retriever())
    
    if query:
        # Retrieve documents related to the query
        context = qa.retriever.get_relevant_documents(query)
        context_text = " ".join([doc.page_content for doc in context])

        # Send the combined context and query to the Ollama model
        prompt = f"""Answer the following question based on the provided context:
        
        <context>
        {context_text}
        </context>
        
        Question: {query}"""

        # Make the request to Ollama
        try:
            answer = query_ollama(model_name, prompt)
            st.write(answer[:500])  # Display the first 500 characters
            
            # Check if the answer exceeds the displayed limit
            if len(answer) > 500:
                if st.button("Continue"):
                    st.write(answer[500:])
        except requests.exceptions.RequestException as e:
            st.write("Error communicating with Ollama:", e)
