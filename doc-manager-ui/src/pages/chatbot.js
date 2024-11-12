// ChatbotUI.js
import React, { useState } from 'react';
import './chatbot.css';

const ChatbotUI = () => {
  const [messages, setMessages] = useState([
    { id: 1, text: 'Hello! How can I assist you today?', isBot: true }
  ]);
  const [input, setInput] = useState('');
  
  const handleSendMessage = () => {
    if (input.trim() === '') return;

    const newMessage = { id: Date.now(), text: input, isBot: false };
    setMessages([...messages, newMessage]);

    // Simulate bot response
    setTimeout(() => {
      setMessages((prev) => [
        ...prev,
        { id: Date.now() + 1, text: 'I’m here to help you manage documents.', isBot: true }
      ]);
    }, 1000);

    setInput('');
  };

  return (
    <div className="app-container">

      <div className="chat-container" >
        <div className="chat-header">Document Management Chatbot</div>

        <div className="chat-history">
          {messages.map((msg) => (
            <div key={msg.id} className={`message ${msg.isBot ? 'bot' : 'user'}`}>
              {msg.text}
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
          <button className="send-button" onClick={handleSendMessage}>Send</button>
        </div>
      </div>


    </div>
  );
};

export default ChatbotUI;
