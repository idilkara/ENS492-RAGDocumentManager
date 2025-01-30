# vector_store.py

from history_manage import get_history, add_to_history
import os
from langchain_chroma import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain.chains import RetrievalQA
from langchain_ollama import OllamaEmbeddings
from langchain_ollama import ChatOllama
from uuid import uuid4
from langchain.schema import Document
import fitz  # PyMuPDF
from documents import add_document_to_mongo, delete_document_from_mongo, is_file_already_uploaded, get_document_by_id
import traceback
from config import EMBEDDING_MODEL_NAME, EMBEDDING_MODEL_URL, CHROMADB_DIR, LLAMA_MODEL
import tempfile
import uuid
from bson import ObjectId
from session_manager import add_message
from langchain.memory import ConversationBufferWindowMemory
from langchain.chains.conversational_retrieval.base import ConversationalRetrievalChain
from langchain.prompts import PromptTemplate



# Initialize embeddings
embeddings = OllamaEmbeddings(base_url=EMBEDDING_MODEL_URL, model=EMBEDDING_MODEL_NAME)


#BUG: ilk seferde db yoksa hata veriyo
os.makedirs(CHROMADB_DIR, exist_ok=True)

# Initialize vector store
vectorstore = Chroma(persist_directory=CHROMADB_DIR, embedding_function=embeddings)


def add_document(file_entry, replace_existing=False):
    """
    Adds a document to the vector store and MongoDB with improved error handling.
    """
    file_data = file_entry["file_data"]
    filename = file_entry["filename"]
    print("Processing document: " + filename)
    temp_file_path = None

    try:
        # Check if file exists
        existing_file = is_file_already_uploaded(filename)
        if existing_file and not replace_existing:
            return {
                "warning": f"File '{filename}' already exists in the system.",
                "options": "Keep the existing file or replace it with the new one."
            }

        # Replace existing file if requested
        if existing_file and replace_existing:
            print(f"Replacing existing file: {filename}")
            delete_document(filename)

        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(filename)[1]) as temp_file:
            temp_file.write(file_data)
            temp_file_path = temp_file.name

        print(f"Temporary File Path: {temp_file_path}")

        # Load and process document
        loader = PyPDFLoader(temp_file_path) if filename.lower().endswith('.pdf') else TextLoader(temp_file_path)
        documents = loader.load()
        print(f"Loaded {len(documents)} document(s) from {filename}")

        # Split into chunks
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        text_chunks = text_splitter.split_documents(documents)
        print(f"Split document into {len(text_chunks)} chunks")

        # Generate document ID and add to MongoDB
        document_id = ObjectId()
        gridfs_id = add_document_to_mongo(temp_file_path, {
            "document_id": document_id,
            "file_name": filename
        })

        print("gridfs in ADD:  ", gridfs_id)

        # Prepare and add documents to vector store
        vector_documents = [
            Document(
                page_content=chunk.page_content,
                metadata={
                    "document_id": str(document_id),
                    "source": filename,
                    "gridfs_id": str(gridfs_id),
                    "file_path": temp_file_path
                }
            )
            for chunk in text_chunks
        ]

        vectorstore.add_documents(vector_documents)
        print(f"Added {len(vector_documents)} documents successfully.")

        return {"message": f"File '{filename}' uploaded successfully.", "gridfs_id": gridfs_id}

    except Exception as e:
        print(f"Error processing document: {str(e)}")
        traceback.print_exc()
        return {"error": str(e)}
    finally:
        # Clean up temporary file
        if temp_file_path and os.path.exists(temp_file_path):
            os.unlink(temp_file_path)

        

# delete docs
def delete_document(file_path):
    """Delete a document from the vector store and the file system."""
    # Remove the file from the db
    delete_document_from_mongo(file_path)
    
    # Remove the document from the vector store
    document_id = None
    dblist = vectorstore.get()
    for item in dblist['metadatas']:
        if item['source'] == file_path:
            document_id = item['document_id']
            break

    if document_id:
        vectorstore.delete_documents([document_id])


def create_qa_chain(vectorstore, llm, memory):
    """
    Creates a ConversationalRetrievalChain with strict context adherence and improved memory management.
    """
    
    # Strict prompt template that enforces using only provided context
    prompt_template = """
    You are a specialized assistant for Sabanci University that ONLY answers questions based on the provided context.
    Use ONLY the following context and chat history to answer the question. 
    If the current question is related to the chat history, you may consider it for better context.
    If the current question is completely unrelated to the chat history, ignore the chat history completely and only use the provided context.
    DO NOT use any other knowledge or information.
    Answer in the same format of the relevant document without skipping relevant parts.
    If the context does not contain information, respond with "I cannot answer this question based on the available context."
    Summarize all key points from the following retrieved context before answering the question.

    Context: {context}
    Chat History: {chat_history}
    Question: {question}

    Answer:"""

    PROMPT = PromptTemplate(
        input_variables=["context", "chat_history", "question"],
        template=prompt_template
    )

    # Configure retriever with similarity search
    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 4}
    )

    # Create chain with memory configuration
    qa_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        memory=memory,
        combine_docs_chain_kwargs={"prompt": PROMPT},
        return_source_documents=True,
        chain_type="stuff",
        verbose=True
    )

    return qa_chain

def search_query(query, user_id, session_id):
    """
    Query the vector store with strict context validation and source checking.
    """
    llm = load_model()
    qa_chain = create_qa_chain(vectorstore, llm, memory=global_memory)
    
    try:
        chat_history = global_memory.load_memory_variables({}).get("chat_history", [])

        # Get the response from the chain using invoke()
        result = qa_chain.invoke({
            "question": query,
            "chat_history": chat_history
        })
        
        # Extract source documents and validate
        source_docs = result.get('source_documents', [])
        
        # If no relevant documents found, return early
        if not source_docs:
            response = "I cannot answer this question based on the available documents."
            add_message(user_id, session_id, query, response)
            return {
                "response": response,
                "file_path": None,
                "highlighted_pdf_path": None,
                "gridfs": None
            }
        
        response = result['answer']
        
        # Get the most relevant chunks for highlighting
        relevant_chunks = source_docs
        
        # Highlight PDF if relevant chunks exist
        highlighted_pdf_path = None
        gridfs_id = None
        if relevant_chunks:
            gridfs_id = relevant_chunks[0].metadata.get("gridfs_id")
            highlighted_pdf_path = highlight_pdf_in_gridfs(gridfs_id, relevant_chunks)
        
        # Add the interaction to message history
        add_message(user_id, session_id, query, response)
        
        return {
            "response": str(response),
            "file_path": str(relevant_chunks[0].metadata.get("file_path")) if relevant_chunks else None,
            "highlighted_pdf_path": str(highlighted_pdf_path) if highlighted_pdf_path else None,
            "gridfs": str(highlighted_pdf_path)
        }
    
    except Exception as e:
        error_msg = f"Error processing query: {str(e)}"
        print(error_msg)
        traceback.print_exc()
        return {"error": error_msg}

# Update the global memory configuration
global_memory = ConversationBufferWindowMemory(
    memory_key="chat_history",
    return_messages=True,
    output_key='answer',
    k=2
)

def get_most_relevant_chunks(query):
    search_results = vectorstore.similarity_search(query)
    return search_results

# # highlighting the most relevant part of the pdf
# # doc.py a alinsa iyi olur
def highlight_pdf_in_gridfs(gridfs_id, relevant_chunks):
    try:
        # Convert gridfs_id from string to ObjectId
        gridfs_id_obj = ObjectId(gridfs_id)

        # Retrieve the PDF from GridFS
        pdf_file = get_document_by_id(gridfs_id_obj)
        if pdf_file is None:
            raise FileNotFoundError(f"File not found in GridFS for ID: {gridfs_id}")

        # Create a temporary file to store the PDF
        temp_pdf_path = f"/tmp/{gridfs_id}_temp.pdf"
        with open(temp_pdf_path, 'wb') as temp_file:
            temp_file.write(pdf_file.read())

        # Verify the temporary file exists
        if not os.path.exists(temp_pdf_path):
            raise FileNotFoundError(f"Temporary file not created: {temp_pdf_path}")

        print(f"Temporary file created at: {temp_pdf_path}")

        # Highlight the relevant parts in the PDF
        highlighted_pdf_path = temp_pdf_path.replace(".pdf", "_highlighted.pdf")
        highlight_text_in_pdf(temp_pdf_path, relevant_chunks, highlighted_pdf_path)

        # Verify the highlighted PDF exists
        if not os.path.exists(highlighted_pdf_path):
            raise FileNotFoundError(f"Highlighted PDF not created: {highlighted_pdf_path}")

        print(f"Highlighted PDF created at: {highlighted_pdf_path}")

        # Store the highlighted PDF back in GridFS
        highlighted_gridfs_id = add_document_to_mongo(highlighted_pdf_path, {
            "document_id": str(uuid.uuid4()),
            "file_name": f"highlighted_{gridfs_id}.pdf",
            "original_gridfs_id": gridfs_id
        })

        # Clean up temporary files
        os.remove(temp_pdf_path)
        os.remove(highlighted_pdf_path)

        return highlighted_gridfs_id

    except Exception as e:
        print(f"Error highlighting PDF: {e}")
        traceback.print_exc()
        return None


def highlight_text_in_pdf(pdf_path, relevant_chunks, output_path):
    print("highlight func a girdiiikkkkk")
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"File not found: {pdf_path}")

    doc = fitz.open(pdf_path)
    print("doc openlandi")
    for page in doc:
        for chunk in relevant_chunks:
            text_instances = page.search_for(chunk.page_content)
            for inst in text_instances:
                # Highlight the found text
                page.add_highlight_annot(inst)

    # Save the highlighted PDF to a new file
    doc.save(output_path, garbage=4, deflate=True)
    doc.close()

    return output_path

def get_vectorstore_dblist():
    return vectorstore.get()


def load_model():
    """
    Load the LLama model with strict system instructions.
    """
    return ChatOllama(
        model=LLAMA_MODEL
    )