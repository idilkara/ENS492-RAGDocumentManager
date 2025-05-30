import React, { useState } from 'react';
import './sidepanel.css';
import Settings from './side-panel-options/sidepanelSettings'; // Import the Settings component
import FileUpload from './side-panel-options/sidepanelupload'; // Import the Settings component
import SUlogo from '../assets/Sabanci_University_logo.png';
import DeleteIcon from "../assets/chat-circle-remove-svgrepo-com.svg"
import CreateIcon from "../assets/chat-circle-add-svgrepo-com.svg"
import ChatsIcon from "../assets/chat-conversation-circle-svgrepo-com.svg"
import SettingsIcon from "../assets/settings-svgrepo-com.svg"
import UploadIcon from "../assets/upload-file-2-svgrepo-com.svg"
import config from "../config";
import apiFetch from '../api';

const SidePanel = ({ chatID, setChatID, sessions, fetchUserSessions, selectedOption, setSelectedOption }) => {
  
  const [showDeleteMsg, setShowDeleteMsg] = useState(false);
  const [sessionToDelete, setSessionToDelete] = useState(null);
  const [deleteAll, setDeleteAll] = useState(false);

  const options = ["Chats", "Manage Documents", "Settings"];
  const optionIcons = [ChatsIcon,  UploadIcon, SettingsIcon];

  const handleDeleteSession = async (sessionId) => {
    if (!sessionId) return;

    const token = localStorage.getItem("authToken");
  
    try {
      const response = await fetch(`${config.API_BASE_URL}/delete_chat_session`, {
        method: "POST",
        headers: {'Content-Type': "application/json", Authorization: `Bearer ${token}`},
        body: JSON.stringify({
          user_id: localStorage.getItem("userId"), // Replace with actual user ID
          session_id: sessionId,
        }),
      });

      const data = await response.json();
      if (response.ok) {
        //fetchUserSessions() REFRESH ATIYOR, main.js'den geldi

        setShowDeleteMsg(false);
        fetchUserSessions();
        setChatID(null);
      } else {
        console.error("Error deleting session:", data.error);
      }
    } catch (error) {
      console.error("Failed to delete chat session:", error);
    }
  };
  
  const handleClearAllSessions = async () => {
    try {
      const data = await apiFetch(`${config.API_BASE_URL}/delete_all_chat_sessions`, {
        method: "POST",
        body: JSON.stringify({ user_id: localStorage.getItem("userId") }), // Replace with actual user ID
      });
  
        setShowDeleteMsg(false);
        fetchUserSessions(); // Refresh the session list
        setChatID(null);


    } catch (error) {
      console.error("Failed to clear all chat sessions:", error);
    }
  };
  

  const renderListingContent = () => {
    switch (selectedOption) {
      case 0: // Saved chats
        return (
          <div className="side-panel-listing">
            <div className="side-panel-listing-createchat" onClick={() => setChatID("NONE")}>
              <div>New Chat</div>
              <img src={CreateIcon} alt="createicon" style={{ width: '20px', height: 'auto' }} />
            </div>
            {sessions
  .slice()
  .sort((a, b) => new Date(b.created_at) - new Date(a.created_at)) // Sort newest first
  .map((session) => (
    <div
    className={`side-panel-listing-element ${chatID === session.session_id ? 'selected-session' : ''}`}
      key={session.session_id}
      onClick={() => setChatID(session.session_id)}
    >
      <div className="side-panel-listing-element-subtitle-container">
        <div className="side-panel-text" > {session.name || "Empty Chat"}</div>
                  <button
              className="icon-button"
              onClick={(e) => {
                e.stopPropagation();  // Prevent opening the session when deleting
                setSessionToDelete(session);
                setShowDeleteMsg(true);
                setDeleteAll(false);
                console.log("Delete Session:", session.session_id);
                //handleDeleteSession(session.session_id);  // Example delete function
              }}
            >

                  <img src={DeleteIcon} alt="deleteicon" style={{ width: '20px', height: 'auto' }} />
                  </button></div>
                {/* <div className="side-panel-listing-element-references">
                  <div className="side-panel-listing-element-reference">Created on: {session.created_at}</div>
                </div> */}
              </div>
            ))}
          </div>
        );
      case 2: // Settings
        return <Settings />; // Render the Settings component
      case 1: // Settings
        return <FileUpload/>; // Render the Settings component
      default:
        return <div className="side-panel-listing">No content available for this option.</div>;
    }
  };
  
return(
<div className="side-panel">
<div className="side-panel-upper">
  <div className="side-panel-title">

  <div className="logo-container">
        <img src={SUlogo} alt="SUlogo" style={{ width: '150px', height: 'auto' }}  />
    </div> 

  <div className="side-panel-title-text">Sabanci University Document Manager</div>


  </div>


</div>



<div className="side-panel-lower">
<div className="side-panel-listing-title">
  {options[selectedOption]}
  {selectedOption === 0 && (
    <span className="clear-all-button" onClick={() => {
      setDeleteAll(true);
      setShowDeleteMsg(true);
    }}>
      Clear All
    </span>
  )}
</div>

  {renderListingContent()}
</div>
<div className="side-panel-bottom">
  <div className="side-panel-options">


    {options.map((option, index) => (
      <div
        key={index}
        className={`side-panel-options-button ${selectedOption === index ? 'active' : ''}`}
        onClick={() => setSelectedOption(index)}
      >
         <img src={optionIcons[index]} alt="deleteicon" style={{ width: '20px', height: 'auto' }}  /> <div>{option}</div>

      </div>
    ))}
  </div>
</div>


{showDeleteMsg && (
        <div className="modal-overlay" onClick={() => setShowDeleteMsg(false)}>
        <div className="modal" onClick={(e) => e.stopPropagation()}>
          <h3>Are you sure?</h3>
          <p>
            {deleteAll
              ? "Do you really want to delete all your previous chats?"
              : `Do you really want to delete chat "${sessionToDelete?.name}"?`}
          </p>
          <div className="modal-buttons">
          <button
                className="confirm-button"
                onClick={() =>
                  deleteAll ? handleClearAllSessions() : handleDeleteSession(sessionToDelete.session_id)
                }
              >
                Yes, Delete
              </button>
              <button className="cancel-button" onClick={() => setShowDeleteMsg(false)}>
                Cancel
              </button> </div>
          </div>
        </div>
      )}


</div>

);
}

export default SidePanel;
