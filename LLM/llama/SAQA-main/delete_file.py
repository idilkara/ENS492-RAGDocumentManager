
import streamlit as st
from langchain.document_loaders import TextLoader
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import LlamaCppEmbeddings
# from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from langchain.embeddings import SentenceTransformerEmbeddings

from langchain.llms import LlamaCpp
from langchain.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings

chromadb = "db"

vectorstore_client = Chroma(persist_directory=chromadb)
db_docs = vectorstore_client.get()

for doc_id, metadata in zip(db_docs["ids"], db_docs["metadatas"]):

        # Delete the document by ID
        vectorstore_client.delete(ids=[doc_id])
        st.write(f"Document has been deleted from the vector database.")
