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

# Initialize vector store
vectorstore = Chroma(persist_directory=CHROMADB_DIR, embedding_function=embeddings)

def add_document(file_entry, replace_existing=False):
    """
    Adds a document to the vector store and MongoDB.
    If the file already exists, prompts the user to decide whether to replace it.
    """
    file_data = file_entry["file_data"]
    filename = file_entry["filename"]
    print("Processing document: " + filename)

    try:
        # Check if the file already exists in MongoDB
        existing_file = is_file_already_uploaded(filename)
        if existing_file and not replace_existing:
            print("file already exists")
            return {
                "warning": f"File '{filename}' already exists in the system.",
                "options": "Keep the existing file or replace it with the new one."
            }

        # If replacing, delete the existing file
        if existing_file and replace_existing:
            print(f"Replacing existing file: {filename}")
            delete_document(filename)

        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(filename)[1]) as temp_file:
            temp_file.write(file_data)
            temp_file_path = temp_file.name

        print(f"Temporary File Path: {temp_file_path}")

        # Choose loader based on file extension
        if filename.lower().endswith('.pdf'):
            loader = PyPDFLoader(temp_file_path)
        else:
            loader = TextLoader(temp_file_path)

        # Load documents
        documents = loader.load()
        print(f"Loaded {len(documents)} document(s) from {filename}")

        # Split documents into chunks
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        text_chunks = text_splitter.split_documents(documents)
        print(f"Split document into {len(text_chunks)} chunks")

        # Generate a MongoDB ObjectId for the document
        document_id = ObjectId()

        # Add to MongoDB GridFS
        gridfs_id = add_document_to_mongo(temp_file_path, {
            "document_id": document_id,
            "file_name": filename
        })

        print("gridfs in ADD:  ", gridfs_id)


        # Prepare documents for vector store
        vector_documents = [
        Document(
            page_content=chunk.page_content,
            metadata={
                "document_id": str(document_id),  # Ensure this is a string
                "source": filename,
                "gridfs_id": str(gridfs_id),  # Ensure this is a string
                "file_path": temp_file_path  # Include the file path
            }
        )
        for chunk in text_chunks
    ]

        # Add documents to vector store
        vectorstore.add_documents(vector_documents)
        print(f"Added {len(vector_documents)} documents successfully.")

        return {"message": f"File '{filename}' uploaded successfully.", "gridfs_id": gridfs_id}

    except Exception as e:
        print(f"Error processing document: {str(e)}")
        traceback.print_exc()  # Print full traceback
        return {"error": str(e)}
    finally:
        # Clean up temporary file
        if 'temp_file_path' in locals() and os.path.exists(temp_file_path):
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


def create_qa_chain(vectorstore, llm):
    """
    Creates a ConversationalRetrievalChain with improved memory and context management.
    """
    # Use WindowMemory to limit the conversation history
    memory = ConversationBufferWindowMemory(
        memory_key="chat_history",
        return_messages=True,
        output_key='answer',
        k=2  # Only keep last 2 interactions
    )

    # Updated prompt template with better context management
    prompt_template = """
    Answer the question based on the following context and recent conversation history.
    If asking for a longer answer, expand on the details from the relevant context.
    If asking for a shorter answer, summarize the key points from the relevant context.
    If the context is not relevant to the question, respond with: "I cannot answer this question based on the available context."
    Only use information from the relevant context.

    Recent Context: {context}
    Recent Chat History: {chat_history}
    Current Question: {question}

    Provide a direct, concise answer:"""

    PROMPT = PromptTemplate(
        input_variables=["context", "chat_history", "question"],
        template=prompt_template
    )

    # Create the chain with modified settings
    qa_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(
            search_kwargs={"k": 2}  # Limit to 2 most relevant documents
        ),
        memory=memory,
        combine_docs_chain_kwargs={"prompt": PROMPT},
        return_source_documents=True,
        verbose=True
    )

    return qa_chain



#BUG : doc yoksa yine de cevap veriyo mu?
def search_query(query, user_id, session_id):
    """Query the vector store with history context and retrieve the relevant document file path."""
    
    llm = load_model()
    qa_chain = create_qa_chain(vectorstore, llm)
    
    # Get the response from the chain
    result = qa_chain({"question": query})
    
    # Extract the response and source documents
    response = result['answer']
    source_docs = result.get('source_documents', [])
    print("SOURCEDOCS????  ", source_docs)
    
    # Get the most relevant chunks for highlighting
    relevant_chunks = source_docs if source_docs else get_most_relevant_chunks(query)
    
    # Highlight PDF if relevant chunks exist
    highlighted_pdf_path = None
    gridfs_id = None
    if relevant_chunks:
        gridfs_id = relevant_chunks[0].metadata.get("gridfs_id")
        highlighted_pdf_path = highlight_pdf_in_gridfs(gridfs_id, relevant_chunks)
    
    # Add the interaction to your existing message history
    add_message(user_id, session_id, query, response)
    
    return {
        "response": str(response),
        "file_path": str(relevant_chunks[0].metadata.get("file_path")) if relevant_chunks else None,
        "highlighted_pdf_path": str(highlighted_pdf_path) if highlighted_pdf_path else None,
        "gridfs": str(highlighted_pdf_path)
    }

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
    return ChatOllama(model=LLAMA_MODEL)
