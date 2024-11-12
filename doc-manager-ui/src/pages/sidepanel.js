// sidepanel.js
import React from 'react';
import './sidepanel.css';
import './chatbot.css';

const SidePanel = ({ isOpen }) => {
      // Log the value of isOpen to check its state
  console.log("isOpen:", isOpen);
  return (
    
    <div className={`side-panel ${isOpen ? 'open' : ''}`}>
      <h2>Chatbot Assistant</h2>
      <p>This panel can contain extra information or settings.</p>
    </div>
  );
};

export default SidePanel;
