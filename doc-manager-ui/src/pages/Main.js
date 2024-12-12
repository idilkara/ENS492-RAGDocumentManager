import React, { useState } from 'react';
import ChatbotUI from './chatbot'; // Assuming ChatbotUI is defined in 'chatbot.js'
import SidePanel from './sidepanel'; // Assuming SidePanel is defined in 'sidepanel.js'
import './Main.css';

const Main = () => {
  const [chatID, setChatID] = useState("NONE");
  console.log('Rendering Main Component with chatID:', chatID);

  return (
    <div className="main-container">
      {/* Left Panel */}
      <div className="left-panel">
        <SidePanel chatID={chatID} />
      </div>

      {/* Right Panel */}
      <div className="right-panel">
        <ChatbotUI chatID={chatID} />
      </div>
    </div>
  );
};

export default Main;
