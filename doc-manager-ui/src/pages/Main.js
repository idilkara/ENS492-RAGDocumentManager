import React, { useState } from 'react';
import ChatbotUI from './chatbot';
import SidePanel from './sidepanel';
import './Main.css';

const Main = () => {
  const [chatID, setChatID] = useState("NONE"); // Shared state for selected chat

  const dummyChats = {
    "chat1": [
      { id: 1, text: "Welcome back to Chat 1!", isBot: true },
      { id: 2, text: "How can I assist you today?", isBot: true },
    ],
    "chat2": [
      { id: 1, text: "Here are some tips to get started.", isBot: true },
        {id: 3, text: "aaaaaa", isBot: false }
    ],
    "chat3": [
      { id: 1, text: "Welcome back to Chat 3!", isBot: true },
        {id: 3, text: "assasasas", isBot: false }
    ],
    "NONE": [
      { id: 1, text: "Hello! How can I assist you today?", isBot: true },
    ],
  };

  return (
    <div className="main-container">
      {/* Pass chatID and setChatID to both components */}
      <div className="left-panel">
        <SidePanel chatID={chatID} setChatID={setChatID} />
      </div>
      <div className="right-panel">
        <ChatbotUI chatID={chatID} chats={dummyChats} />
      </div>
    </div>
  );
};

export default Main;
