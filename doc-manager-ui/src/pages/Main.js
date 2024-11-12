import React, { useState } from 'react';
import ChatbotUI from './chatbot'; // Assuming the ChatbotUI component is in 'chatbot.js'
import SidePanel from './sidepanel'; // Assuming the SidePanel component is in 'sidepanel.js'

const Main = () => {
  const [isPanelOpen] = useState(true); // Toggle this state to open/close the panel

  console.log('Rendering Main Component');

  return (


    <div className="main-container">
          {/* Left panel - Pink */}


          <SidePanel isOpen={isPanelOpen} />

        

          <ChatbotUI />

        </div>
  );
};

export default Main;
