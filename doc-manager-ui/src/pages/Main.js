import React, { useState } from 'react';
import ChatbotUI from './chatbot';
import SidePanel from './sidepanel';

const Main = () => {
  const [isPanelOpen, setIsPanelOpen] = useState(false);

  console.log('Rendering Main Component');
  
  return (
    <div className="main-container">
      <ChatbotUI isPanelOpen={isPanelOpen} setIsPanelOpen={setIsPanelOpen} />
      
      {/* Render the SidePanel outside the button */}
      <SidePanel isOpen={isPanelOpen} /> {/* Pass the isOpen prop to the SidePanel */}
      
      <button
        className="toggle-panel-button"
        style={{ left: isPanelOpen ? '300px' : '0' }}
        onClick={() => setIsPanelOpen(!isPanelOpen)} // Toggle the panel state
      >
        {isPanelOpen ? 'Close Panel' : 'Open Panel'}
      </button>
    </div>
  
  );
};

export default Main;
