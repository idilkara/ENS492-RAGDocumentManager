import React, { useState, useRef, useEffect } from "react";
import ReactMarkdown from "react-markdown";
import './chatbot.css';
import axios from 'axios';
import config from "../config";
import apiFetch from "../api";

const ChatbotUI = ({ chatID, chats, createNewChatSession, setChats, setChatID }) => {
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState(chats[chatID] || []);
  const chatHistoryRef = useRef(null);
  const [isSending, setIsSending] = useState(false);

  const [selectedModel, setSelectedModel] = useState("llama3.2:3b"); // Default model
  const models = ["llama3.2:3b", "llama3.3:7b", "deepseek-r1:1.5b", "mistral:7b"]; // get it from frontend

  const chatIdRef = useRef(chatID);

useEffect(() => {
  chatIdRef.current = chatID;
}, [chatID]);


const handleSendMessage = async () => {
  if (input.trim() === "" || isSending) return;

  setIsSending(true);

  let currentChatId = chatID;
  const userMessage = { id: Date.now(), text: input, isBot: false };

  // If chatID is null, create a new chat session
  if (!currentChatId) {
    try {
      currentChatId = await createNewChatSession();
      if (!currentChatId) {
        setMessages((prev) => [
          ...prev,
          { id: Date.now() + 1, text: "Error creating new chat session. Please try again.", isBot: true },
        ]);
        setIsSending(false);
        return;
      }
      
      // Ensure we don't overwrite messages with a new array if it already exists
      setChats(prev => ({
        ...prev,
        [currentChatId]: prev[currentChatId] || []  // Only set if it doesn't exist
      }));

      setChatID(currentChatId); // Update chat ID state immediately
    } catch (error) {
      console.error("Error creating new chat session:", error);
      setIsSending(false);
      return;
    }
  }

  // Add the user message **only once** (outside session creation logic)
  setMessages((prev) => [...prev, userMessage]);
  setChats(prev => ({
    ...prev,
    [currentChatId]: [...(prev[currentChatId] || []), userMessage]  // Ensure it appends correctly
  }));

  setInput("");

  try {
    const data = await apiFetch(`${config.API_BASE_URL}/user_query`, {
      method: 'POST',
      body: JSON.stringify({
        query: input,
        user_id: localStorage.getItem("userId"),
        session_id: currentChatId,
        model: selectedModel
      })
    });

    const botResponse = typeof data.response === 'string' ? data.response : JSON.stringify(data.response);
    const highlightedPdfsource= data.source_docs_arr|| null;
    console.log(data);
    console.log(highlightedPdfsource);

    const botMessageId = Date.now() + 1;
    const botMessage = { id: botMessageId, text: "", isBot: true, sources:  highlightedPdfsource };

    // Append bot message
    setMessages((prev) => [...prev, botMessage]);
    setChats(prev => ({
      ...prev,
      [currentChatId]: [...prev[currentChatId], botMessage]
    }));

    // Simulate streaming effect
    const words = botResponse.split(" ");
    for (let i = 0; i < words.length; i++) {
      await new Promise((resolve) => setTimeout(resolve, 50));

      setMessages((prevMessages) =>
        prevMessages.map((msg) =>
          msg.id === botMessageId ? { ...msg, text: (msg.text || "") + words[i] + " " } : msg
        )
      );

      setChats(prev => ({
        ...prev,
        [currentChatId]: prev[currentChatId].map((msg) =>
          msg.id === botMessageId ? { ...msg, text: (msg.text || "") + words[i] + " " } : msg
        )
      }));
    }

  } catch (error) {
    console.error("Error sending request:", error);
    const errorMessage = { 
      id: Date.now() + 1, 
      text: "Sorry, there was an issue processing your request.", 
      isBot: true 
    };
    setMessages((prev) => [...prev, errorMessage]);
    setChats(prev => ({
      ...prev,
      [currentChatId]: [...prev[currentChatId], errorMessage]
    }));
  }
  setIsSending(false);
};



const handleViewPDFClick = async (pdfPath, pageNumber = 1) => {
  if (!pdfPath) return;

  const token = localStorage.getItem('authToken');
  
  try {
    const response = await axios.get(
      `${config.API_BASE_URL}/get_highlighted_pdf?file_path=${encodeURIComponent(pdfPath)}`,
      {
        responseType: 'blob',
        headers: {'Authorization': `Bearer ${token}`}
      }
    );
    
    const blob = new Blob([response.data], { type: 'application/pdf' });
    const url = window.URL.createObjectURL(blob);
    
    // Open the PDF in a new tab with the specific page number
    window.open(`${url}#page=${pageNumber}`, "_blank");
    
    // Clean up the URL object after opening
    setTimeout(() => {
      window.URL.revokeObjectURL(url);
    }, 100);
  } catch (error) {
    if (error.response && error.response.status === 404) {
      alert("The highlighted PDF has expired. Please make the query again to generate a new highlight.");
    } else {
      console.error("Error fetching PDF:", error);
      alert("Error loading the PDF. Please try again.");
    }
  }
};

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  // Scroll to the most recent message
  useEffect(() => {
    if (chatHistoryRef.current) {
      chatHistoryRef.current.scrollTop = chatHistoryRef.current.scrollHeight;
    }
  }, [messages]);

  useEffect(() => {
    setMessages(chats[chatID] || []);
  }, [chatID, chats]);



  return (
    <div className="chat-interaction-container">
      <div className="chat-container">

      <div className="chat-header">
      <select
        className="model-select"
        value={selectedModel}
        onChange={(e) => setSelectedModel(e.target.value)}
      >
        {models.map((model) => (
          <option key={model} value={model}>
            {model}
          </option>
        ))}
      </select>
          You are speaking with ✨ {selectedModel} ✨
      </div>
        <div className="chat-history" ref={chatHistoryRef}>
          {messages.length === 0 ? (
          

              <div  className="message bot">
             <ReactMarkdown>Hello! Let me know what you're curious about, and I'll find the relevant documents for you. How can I help you?</ReactMarkdown> 
              </div>
          ) : (
            messages.map((msg) => (
              <div key={msg.id} className={`message ${msg.isBot ? 'bot' : 'user'}`}>
                <ReactMarkdown>{msg.text}</ReactMarkdown>
          
                {msg.isBot && msg.sources && msg.sources.length > 0 && (
                  msg.sources
                  .filter(source => source?.filename && source.filename !== "No filename") // Ensure filename is valid
                  .map((source, index) => (
                      <button
                        key={index}
                        className="display-button"
                        onClick={() => handleViewPDFClick(source.highlighted_pdf_path, source.pages[0])}
                      >
                        <div className="pdfLabel">{source.filename}</div>
                      </button>
                    ))
                )}



              </div>
            ))
          )}
        </div>
        <div className="input-container">
          <textarea
            className="text-input"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Type your message..."
            disabled={isSending}
          />
          <button className="send-button" onClick={handleSendMessage} disabled={isSending}>
            {isSending ? "Waiting..." : "Send"}
          </button>
        </div>
        <div className="feedback-link">
      <a href="https://docs.google.com/forms/d/e/1FAIpQLSedQob3XPLOoiyA3sLy7jsVG0L3twcE_upSVL7ezV7NSuSVYQ/viewform?usp=header" target="_blank" rel="noopener noreferrer">
        Give us feedback!
      </a>
</div>

      </div>
    </div>
  );
  


};

export default ChatbotUI;