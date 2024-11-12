import React, { useState } from 'react';
import './chatbot.css';

const ChatbotUI = () => {
  const [messages, setMessages] = useState([
    { id: 1, text: 'Hello! How can I assist you today?', isBot: true },
  ]);
  const [input, setInput] = useState('');
  const [isDimVisible, setIsDimVisible] = useState(false);  // State for dim overlay visibility
  const [isPdfVisible, setIsPdfVisible] = useState(false);  // State for PDF visibility

  const handleSendMessage = () => {
    if (input.trim() === '') return;

    const newMessage = { id: Date.now(), text: input, isBot: false };
    setMessages([...messages, newMessage]);

    // Simulate bot response
    setTimeout(() => {
      setMessages((prev) => [
        ...prev,
        { id: Date.now() + 1, text: 'I’m here to help you manage documents.', isBot: true },
      ]);
    }, 1000);

    setInput('');
  };

  const handleViewPDFClick = () => {
    setIsDimVisible(true);  // Show dim overlay when the button is clicked
    setIsPdfVisible(true);  // Show PDF viewer
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
        <div className="chat-header">Document Management Chatbot</div>

        <div className="chat-history">
          {messages.map((msg) => (
            <div key={msg.id} className={`message ${msg.isBot ? 'bot' : 'user'}`}>
              {msg.text}

              {/* Show the button below the chatbot message only */}
              {msg.isBot && (
                <button className="display-button" onClick={handleViewPDFClick}>
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
