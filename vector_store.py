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
from highlight_pdf_handle import TempFileManager, PDFHighlighter
from langchain_experimental.text_splitter import SemanticChunker
import re


temp_file_manager = TempFileManager()
pdf_highlighter = PDFHighlighter(temp_file_manager)



# Initialize embeddings
embeddings = OllamaEmbeddings(base_url=EMBEDDING_MODEL_URL, model=EMBEDDING_MODEL_NAME)


#BUG: ilk seferde db yoksa hata veriyo
os.makedirs(CHROMADB_DIR, exist_ok=True)

# Initialize vector store
vectorstore = Chroma(persist_directory=CHROMADB_DIR, embedding_function=embeddings)

def adaptive_document_splitter(documents, max_chunk_size=1000):
    def is_header(text):
        return bool(re.match(r"^(\#{1,6} |\d+\. |[A-Z][A-Za-z0-9\s]+$)", text.strip()))
    
    adaptive_chunks = []
    current_header = None
    grouped_text = []
    
    for doc in documents:
        lines = doc.page_content.split("\n")
        metadata = doc.metadata.copy()
        
        for line in lines:
            if is_header(line):
                if grouped_text:
                    chunk_text = "\n".join(grouped_text)
                    if current_header:
                        chunk_text = f"{current_header}\n{chunk_text}"
                    adaptive_chunks.append(Document(page_content=chunk_text, metadata=metadata))
                
                current_header = line.strip()
                grouped_text = []
            else:
                grouped_text.append(line)
        
        if grouped_text:
            chunk_text = "\n".join(grouped_text)
            if current_header:
                chunk_text = f"{current_header}\n{chunk_text}"
            adaptive_chunks.append(Document(page_content=chunk_text, metadata=metadata))
    
    return adaptive_chunks


def add_document(file_entry, replace_existing=False):
    """
    Adds a document to the vector store and MongoDB.
    """
    file_data = file_entry["file_data"]
    filename = file_entry["filename"]
    print("Processing document: " + filename)
    temp_file_path = None

    try:
        # Create temporary file to process the PDF
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
            temp_file_path = temp_file.name
            temp_file.write(file_data)

        # Store in MongoDB
        mongo_id = add_document_to_mongo(file_data, filename)
        if not mongo_id:
            raise Exception("Failed to store document in MongoDB")

        print("mongo_id: ", mongo_id)

        # chunker = SemanticChunker(embeddings)

        # Load and process document
        loader = PyPDFLoader(temp_file_path) if filename.lower().endswith('.pdf') else TextLoader(temp_file_path)
        documents = loader.load()
        print(f"Loaded {len(documents)} document(s)")

        # Split into semantic chunks
        text_chunks = adaptive_document_splitter(documents)
        print(f"Split into {len(text_chunks)} chunks")

        # Prepare documents for vector store
        vector_documents = [
            Document(
                page_content=chunk.page_content,
                metadata={
                    "source": filename,
                    "mongo_id": mongo_id,
                    "temp_path": temp_file_path
                }
            )
            for chunk in text_chunks
        ]

        # Add to vector store
        vectorstore.add_documents(vector_documents)
        print(f"Added {len(vector_documents)} documents to vector store")

        return {"message": f"File '{filename}' uploaded successfully", "mongo_id": mongo_id}

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

#TODO : memory yi simdilik sildim eklenecek
def create_qa_chain(vectorstore, llm):
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
    You can engage in casual conversation but professionally
    Context: {context}
   
    Question: {question}

    Answer:"""

    PROMPT = PromptTemplate(
        input_variables=["context", "question"],
        template=prompt_template
    )

    # Configure retriever with similarity search
    retriever = vectorstore.as_retriever(
        search_type="mmr",
        search_kwargs={"k": 5, "fetch_k": 20},
    )

    # Create chain with memory configuration
    qa_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        memory=global_memory,
        combine_docs_chain_kwargs={"output_key": "answer"},
        return_source_documents=True,
        chain_type="stuff",
        verbose=True
    )

    return qa_chain



def search_query(query, user_id, session_id):
    """
    Query the vector store and return results with highlighted PDFs.
    """
    llm = load_model()
    qa_chain = create_qa_chain(vectorstore, llm)
   
    try:
        print(f"\nQuery: {query}")

        # # Get the most relevant chunks before QA
        # relevant_chunks = vectorstore.similarity_search(query, k=8)
        # print("\nRetrieved chunks:")
        # for i, chunk in enumerate(relevant_chunks):
        #     print(f"\nChunk {i+1}:")
        #     print(f"Source: {chunk.metadata.get('source')}")
        #     print(f"Content: {chunk.page_content[:200]}...")  # First 200 chars

       
        result = qa_chain.invoke({
            "question": query,
            "chat_history": global_memory
        })
       
        source_docs = result.get('source_documents', [])
        print(len(source_docs[:2]))
        print("source docs::::  ", source_docs[:2])
        if not source_docs:
            response = "I cannot answer this question based on the available documents."
            add_message(user_id, session_id, query, response)
            return {
                "response": response,
                "highlighted_pdf_path": None
            }
       
        response = result['answer']
       
        # Create highlighted PDF if relevant chunks exist
        highlighted_pdf_path = None
        if source_docs:
            mongo_id = source_docs[0].metadata.get("mongo_id")
            print(f"MongoDB document ID: {mongo_id}")
           
            if mongo_id:
                highlighted_pdf_path = create_highlighted_pdf(mongo_id, source_docs[:2])
                print(f"Highlighted PDF path: {highlighted_pdf_path}")
       
        # Add the interaction to message history
        add_message(user_id, session_id, query, response)
       
        return {
            "response": str(response),
            "highlighted_pdf_path": highlighted_pdf_path if highlighted_pdf_path else None
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
    input_key = 'question',
    output_key='answer',
    k=3
)

def get_most_relevant_chunks(query):
    search_results = vectorstore.similarity_search(query)
    return search_results


def create_highlighted_pdf(mongo_id, relevant_chunks):
    return pdf_highlighter.create_highlighted_pdf(mongo_id, relevant_chunks)


# # highlighting the most relevant part of the pdf
# # doc.py a alinsa iyi olur
# def create_highlighted_pdf(mongo_id, relevant_chunks):
#     """
#     Creates a highlighted version of a PDF file from MongoDB document.
#     """
#     temp_original_path = None
#     try:
#         # Get document from MongoDB
#         document = get_document_by_id(mongo_id)
#         if not document:
#             print(f"Document not found in MongoDB with ID: {mongo_id}")
#             return None

#         # Create temporary file for the original PDF
#         with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
#             temp_original_path = temp_file.name
#             temp_file.write(document['file_data'])

#         # Generate path for highlighted PDF in temp directory
#         highlighted_pdf_path = temp_file_manager.get_temp_filepath()

#         # Highlight the relevant parts in the PDF
#         try:
#             highlight_text_in_pdf(temp_original_path, relevant_chunks, highlighted_pdf_path)
#             print(f"Created highlighted PDF at: {highlighted_pdf_path}")
#         except Exception as e:
#             print(f"Error during highlighting: {e}")
#             if os.path.exists(highlighted_pdf_path):
#                 os.remove(highlighted_pdf_path)
#             return None

#         # Register the highlighted PDF with the temp file manager
#         temp_file_manager.add_file(highlighted_pdf_path)

#         return highlighted_pdf_path

#     except Exception as e:
#         print(f"Error highlighting PDF: {e}")
#         traceback.print_exc()
#         return None
#     finally:
#         # Clean up temporary original file
#         if temp_original_path and os.path.exists(temp_original_path):
#             os.unlink(temp_original_path)



# def highlight_text_in_pdf(pdf_path, relevant_chunks, output_path):
#     print("highlight func a girdiiikkkkk")
#     if not os.path.exists(pdf_path):
#         raise FileNotFoundError(f"File not found: {pdf_path}")

#     doc = fitz.open(pdf_path)
#     print("doc openlandi")
#     for page in doc:
#         for chunk in relevant_chunks:
#             text_instances = page.search_for(chunk.page_content)
#             for inst in text_instances:
#                 print("HIGHLIGHT PART: ", inst)
#                 # Highlight the found text
#                 page.add_highlight_annot(inst)

#     # Save the highlighted PDF to a new file
#     doc.save(output_path, garbage=4, deflate=True)
#     doc.close()

#     return output_path

def load_model():
    """
    Load the LLama model.
    """
    return ChatOllama(
        model=LLAMA_MODEL
    )