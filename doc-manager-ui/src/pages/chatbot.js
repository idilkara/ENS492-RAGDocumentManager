import React, { useState, useRef, useEffect } from "react";
import ReactMarkdown from "react-markdown";
import './chatbot.css';
import axios from 'axios';

const ChatbotUI = ({ chatID, chats }) => {
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState(chats[chatID] || []);
  const chatHistoryRef = useRef(null);

  const handleSendMessage = async () => {
    if (input.trim() === "") return;
    
    const userMessage = { id: Date.now(), text: input, isBot: false };
    setMessages((prev) => [...prev, userMessage]);
    
    try {
      const response = await axios.post("http://127.0.0.1:5000/user_query", {
        query: input,
        user_id: '1',
        session_id: chatID
      });
      
      const data = response.data;
      const botResponse = typeof data.response === 'string' ? data.response : JSON.stringify(data.response);
      const highlightedPdfPath = data.highlighted_pdf_path || null;
      
      const botMessageId = Date.now() + 1;

      console.log("Highlighted PDF Path:", highlightedPdfPath);
      setMessages((prev) => [
        ...prev,
        { id: botMessageId, text: "", isBot: true, pdfPath: highlightedPdfPath }
      ]);

      // Simulate streaming effect
      const words = botResponse.split(" ");
      for (let i = 0; i < words.length; i++) {
        await new Promise((resolve) => setTimeout(resolve, 50)); // Adjust speed here

        setMessages((prevMessages) =>
          prevMessages.map((msg) =>
            msg.id === botMessageId
              ? { ...msg, text: prevMessages.find((m) => m.id === botMessageId).text + words[i] + " " }
              : msg
          )
        );
      }
    } catch (error) {
      console.error("Error sending request:", error);
      setMessages((prev) => [
        ...prev,
        { id: Date.now() + 1, text: "Sorry, there was an issue processing your request.", isBot: true },
      ]);
    }

    setInput("");
  };

  const handleViewPDFClick = async (pdfPath) => {
    if (!pdfPath) return;
    
    try {
      const response = await axios.get(
        `http://127.0.0.1:5000/get_highlighted_pdf?file_path=${encodeURIComponent(pdfPath)}`,
        {
          responseType: 'blob',
        }
      );
      
      const blob = new Blob([response.data], { type: 'application/pdf' });
      const url = window.URL.createObjectURL(blob);
      
      // Open the PDF in a new tab
      window.open(url, "_blank");
      
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
        <div className="chat-history" ref={chatHistoryRef}>
          {messages.map((msg) => (
            <div key={msg.id} className={`message ${msg.isBot ? 'bot' : 'user'}`}>
              <ReactMarkdown>{msg.text}</ReactMarkdown>
              {msg.isBot && msg.pdfPath && (
                <button 
                  className="display-button" 
                  onClick={() => handleViewPDFClick(msg.pdfPath)}
                >
                  <div className="pdfLabel">View Highlighted PDF</div>
                </button>
              )}
            </div>
          ))}
        </div>
        <div className="input-container">
          <textarea
            className="text-input"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Type your message..."
          />
          <button className="send-button" onClick={handleSendMessage}>
            Send
          </button>
        </div>
        <div className="feedback-link">Give us feedback!</div>
      </div>
    </div>
  );
};

export default ChatbotUI;