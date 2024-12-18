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

const SidePanel = ({ chatID, setChatID, sessions }) => {
  const [selectedOption, setSelectedOption] = useState(0);
  const options = ["Chats", "Upload a document", "Settings"];
  const optionIcons = [ChatsIcon, SettingsIcon, UploadIcon];

  const renderListingContent = () => {
    switch (selectedOption) {
      case 0: // Saved chats
        return (
          <div className="side-panel-listing">
            <div className="side-panel-listing-createchat" onClick={() => setChatID("NONE")}>
              <div>New Chat</div>
              <img src={CreateIcon} alt="createicon" style={{ width: '20px', height: 'auto' }} />
            </div>
            {sessions.map((session) => (
              <div className="side-panel-listing-element" key={session.session_id} onClick={() => setChatID(session.session_id)}>
                <div className="side-panel-listing-element-subtitle-container">
                  <div>{session.name}</div> <img src={DeleteIcon} alt="deleteicon" style={{ width: '20px', height: 'auto' }} />
                </div>
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

  <div className="side-panel-title-text">Document Management System</div>


  </div>


</div>



<div className="side-panel-lower">
  <div className="side-panel-listing-title">{options[selectedOption]}    </div>
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
</div>
);
}

export default SidePanel;
