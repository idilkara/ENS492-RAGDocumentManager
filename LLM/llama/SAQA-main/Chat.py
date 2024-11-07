# Chat.py
# Import necessary libraries
import os
import streamlit as st
from langchain.llms import LlamaCpp
from langchain.vectorstores import Chroma
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.chains import RetrievalQA
from langchain_ollama import OllamaEmbeddings
from langchain_ollama import ChatOllama


# used to create the memory
from langchain.memory import ConversationBufferMemory
memory_key = "history"

"""## Local LLM 
base_dir = "..\\llms\\llama2\\" 
llm_model = "llama-2-7b-chat.ggmlv3.q5_K_M.bin"
local_llm = base_dir+llm_model
"""


## Vector Database 
chromadb = "db"
upload_folder = "upload"
os.makedirs(upload_folder, exist_ok=True)
embeddings = OllamaEmbeddings(base_url="http://localhost:11434", model="nomic-embed-text")
vectorstore = Chroma(persist_directory=chromadb, embedding_function=embeddings)

def load_model():

    llm = ChatOllama(
        model="llama3.2:3b",
    )
    return llm

# Memory is added to an agent to take it from being stateless to stateful i.e. it remembers previous interactions. 
# This means you can ask follow-up questions, making interaction with the agent much more efficient and feel more natural.

memory = ConversationBufferMemory(memory_key=memory_key, return_messages=True)


# Streamlit UI
# st.image('images\idesign.png', width=400)
st.header("AI Assistant")
query = st.text_input("Enter your query")


if st.button("Retrieve"):
    llm = load_model()
    qa = RetrievalQA.from_llm(llm, retriever=vectorstore.as_retriever())
    if query:
        results = qa(query)
        print(len(results))
        answer = results['result']
        print(answer)

        # Display the first part of the answer
        st.write(answer)  # Display the first 500 characters, adjust as needed

        # Check if the answer exceeds the displayed limit
        # LEN DEGISECEKKK COK AZZ
        if len(answer) > 10000:
            # Display "Continue" button
            if st.button("Continue"):
                # Display the rest of the answer
                st.write(answer[500:])  # Display the rest of the answer

