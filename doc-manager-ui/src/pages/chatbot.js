import React, { useState } from 'react';
import './chatbot.css';
import axios from 'axios';

const ChatbotUI = () => {
  const [messages, setMessages] = useState([
    { id: 1, text: 'Hello! How can I assist you today?', isBot: true },
  ]);
  const [input, setInput] = useState('');
  const [isDimVisible, setIsDimVisible] = useState(false);  // State for dim overlay visibility
  const [isPdfVisible, setIsPdfVisible] = useState(false);  // State for PDF visibility

  const handleSendMessage = async () => {
    if (input.trim() === "") return;

    const userMessage = { id: Date.now(), text: input, isBot: false };
    setMessages((prev) => [...prev, userMessage]);

    try {
      const response = await axios.post("http://127.0.0.1:5000/user_query", {
        query: input
      });

      const data = response.data;

      const botResponse = typeof data.response === 'string' ? data.response : JSON.stringify(data.response);
      const filePath = data.file_path || null;

      // Ensure file path is handled separately
      setMessages((prev) => [
        ...prev,
        {
          id: Date.now() + 1,
          text: botResponse,  // Only response, no file path in text
          isBot: true,
          filePath: filePath, // Store filePath separately for the "View PDF" button
        },
      ]);
    } catch (error) {
      console.error("Error sending request:", error);
      setMessages((prev) => [
        ...prev,
        { id: Date.now() + 1, text: "Sorry, there was an issue processing your request.", isBot: true },
      ]);
    }

    setInput("");
  };

  const handleViewPDFClick = async (filePath) => {
    if (!filePath) return;

    try {
      const response = await axios.get(`http://127.0.0.1:5000/get_pdf?file_path=${encodeURIComponent(filePath)}`, {
        responseType: 'blob',
      });

      const blob = new Blob([response.data], { type: 'application/pdf' });
      const url = window.URL.createObjectURL(blob);

      // Open the PDF in a new tab
      window.open(url, "_blank");
    } catch (error) {
      console.error("Error fetching PDF:", error);
    }
  };

  const handleBackArrowClick = () => {
    setIsDimVisible(false);  // Hide dim overlay when back arrow is clicked
    setIsPdfVisible(false);  // Hide PDF viewer
  };

  return (
    <div className="app-container">
      {isDimVisible && (
        <div className="dim">
          {/* Back arrow button to restore lights */}
          <button className="back-arrow-button" onClick={handleBackArrowClick}>
            ←
          </button>
        </div>
      )}

      {/* PDF Viewer */}
      {isPdfVisible && (
        <div className="pdf-container">
          {/* Using iframe to display the PDF */}
          <iframe
            src="/pdfs/aaa.pdf"  // Assuming the PDF is in the public folder
            title="PDF Viewer"
          ></iframe>
        </div>
      )}

      <div className="chat-container">
        <div className="chat-header">SUDoc</div>

        <div className="chat-history">
          {messages.map((msg) => (
            <div key={msg.id} className={`message ${msg.isBot ? 'bot' : 'user'}`}>
              {msg.text}

              {/* Show the button below the chatbot message only if filePath exists */}
              {msg.isBot && msg.filePath && (
                <button className="display-button" onClick={() => handleViewPDFClick(msg.filePath)}>
                  View PDF
                </button>
              )}
            </div>
          ))}
        </div>

        <div className="input-container">
          <input
            type="text"
            className="text-input"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Type your message..."
          />
          <button className="send-button" onClick={handleSendMessage}>
            Send
          </button>
        </div>
      </div>
    </div>
  );
};

export default ChatbotUI;
