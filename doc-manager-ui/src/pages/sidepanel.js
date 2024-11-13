import React, { useState } from 'react';
import './sidepanel.css';

const SidePanel = ({ isOpen }) => {
  // State to hold the feedback message
  const [message, setMessage] = useState("");

  // Handlers to update the message
  const handleSavedChatsClick = () => {
    setMessage("Saved Chats");
    // Additional functionality for opening saved chats can go here
  };

  const handleStarredDocumentsClick = () => {
    setMessage("Starred Documents");
    // Additional functionality for starred documents can go here
  };

  const handleSettingsClick = () => {
    setMessage("Settings");
    // Additional functionality for settings can go here
  };

  return (
    <div className={`side-panel ${isOpen ? 'open' : ''}`}>
      <h2>Your Space</h2>

      {/* Display feedback message here */}
      <p className="feedback-message">{message}</p>

      {/* Navigation bar at the bottom */}
      <div className="side-panel-nav">
        <div className="nav-item" onClick={handleSavedChatsClick}>Saved Chats</div>
        <div className="nav-item" onClick={handleStarredDocumentsClick}>Starred Documents</div>
        <div className="nav-item" onClick={handleSettingsClick}>Settings</div>
      </div>
    </div>
  );
};

export default SidePanel;
