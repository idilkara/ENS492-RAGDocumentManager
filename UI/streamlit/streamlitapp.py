import streamlit as st
import random
import time
import base64

# Set initial page configuration
st.set_page_config(page_title="Doc Chat", page_icon="📚", layout="wide")

      # Custom CSS for glassmorphic effect and modern UI
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Times+New+Roman&display=swap');

    * {
        font-family: 'Times New Roman', serif;
    }

    .stApp {
        background: white;
    }

    .chat-container {
        background: rgba(26, 42, 79, 0.1) !important;
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 25px;
        margin: 15px 0;
       

        color: #1a2a4f;
    }

    .stChatMessage {
        background: rgba(26, 42, 79, 0.1) !important;
        backdrop-filter: blur(10px) !important;
        border-radius: 15px !important;
        
        padding: 15px !important;
        margin: 10px 0 !important;
        
        color: #1a2a4f !important;
          
    }

    .stMarkdown {
        color: #1a2a4f !important;
    }

    h1, h2, h3 {
        color: #1a2a4f !important;
        font-family: 'Times New Roman', serif !important;
        font-weight: 600 !important;
    }

    .upload-container {
        background: rgba(26, 42, 79, 0.1) !important;
        backdrop-filter: blur(10px) !important;
        border-radius: 20px;
        color: #1a2a4f !important;
        padding: 25px;
        margin: 15px 0;
        border: 1px solid rgba(26, 42, 79, 0.2);
       
    }

    .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.8) !important;
        backdrop-filter: blur(10px) !important;
        border: 1px solid rgba(26, 42, 79, 0.2) !important;
        border-radius: 10px !important;
        color: #1a2a4f !important;
        font-family: 'Times New Roman', serif !important;
        padding: 15px !important;
    }

    .stChatInputContainer {
        background: rgba(255, 255, 255, 0.8) !important;
        backdrop-filter: blur(10px) !important;
        border-radius: 15px !important;
        border: 1px solid rgba(26, 42, 79, 0.2) !important;
        padding: 5px !important;
        margin-top: 20px !important;

    }

    .stChatInputContainer textarea {
        color: #1a2a4f !important;
        font-family: 'Times New Roman', serif !important;
    }

    .stButton > button {
        background: rgba(26, 42, 79, 0.1) !important;
        border: 1px solid rgba(26, 42, 79, 0.2) !important;
        border-radius: 10px !important;
        color: #1a2a4f !important;
        font-family: 'Times New Roman', serif !important;
        transition: all 0.3s ease;
        backdrop-filter: blur(10px) !important;
        
    }

    .stButton > button:hover {
        background: rgba(26, 42, 79, 0.2) !important;
        transform: translateY(-2px);
        backdrop-filter: blur(10px) !important;
    }

    /* Sidebar styling */
    .css-1d391kg {
        background: rgba(255, 255, 255, 0.8) !important;
        backdrop-filter: blur(10px) !important;
    }
    
    </style>
    """, unsafe_allow_html=True)


# Initialize session state for login and navigation
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# Sign-In Page Function
def sign_in():
    st.title("Sign In")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Sign In"):
        if (username and
                password):
            st.session_state.logged_in = True
            st.success("Logged in successfully!")
            st.rerun()
        else:
            st.warning("Invalid username or password.")
            st.session_state.logged_in = True
            st.success("Logged in successfully!")
            st.rerun()


# Main Chat Page
def main_app():
    # Sidebar
    with st.sidebar:
        st.markdown("""
            <div class="upload-container">
                <h2>SU Document Management</h2>
            </div>
        """, unsafe_allow_html=True)

    # Initialize session state
    if 'messages' not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "Welcome! How can I assist you with SU documents today?"}]
    if 'documents' not in st.session_state:
        st.session_state.documents = []
    if 'current_input' not in st.session_state:
        st.session_state.current_input = ""

    # Placeholder responses
    placeholder_responses = [
        "I found several relevant sections in your documents. Let me summarize them...",
    ]

    # Main chat interface
    st.markdown("""
        <div class="chat-container">
            <h1>SU Document Assistant</h1>
        </div>
    """, unsafe_allow_html=True)


    # Display the chat messages
    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    # User input for the chat
    if prompt := st.chat_input("Ask something about SU documents..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)


        # Simulate thinking with a spinner
        with st.spinner("Processing..."):
            time.sleep(0.5)
        
        # Generate response
        msg = random.choice(placeholder_responses)
        
        # Add assistant response
        st.session_state.messages.append({"role": "assistant", "content": msg})
        st.chat_message("assistant").write(msg)

        # Display assistant's response in chat
        with st.container():
            path =  '../placeholder-pdfs/meeting-notes.pdf'
            with st.expander("Click to view PDF File"):
                try:
                    with open(path, "rb") as f:
                        pdf_data = f.read()
                        pdf_base64 = base64.b64encode(pdf_data).decode("utf-8")
                        pdf_display = f'<iframe src="data:application/pdf;base64,{pdf_base64}" width="700" height="400" type="application/pdf"></iframe>'
                        st.markdown(pdf_display, unsafe_allow_html=True)
                except FileNotFoundError:
                    st.error("PDF file 'aaa.pdf' not found.")


if not st.session_state.logged_in:
    sign_in()
elif st.session_state.logged_in:
    main_app()