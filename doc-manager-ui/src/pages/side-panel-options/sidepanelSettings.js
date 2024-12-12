import React, { useState } from 'react';
import './sidepanelsettings.css';
const Settings = () => {
    const [theme, setTheme] = useState('Light');
  
    // const toggleTheme = () => {
    //   setTheme(theme === 'Light' ? 'Dark' : 'Light');
    //   document.body.className = theme === 'Light' ? 'dark-mode' : 'light-mode'; // Dynamically update the body class
    // };
  
    return (
      <div className="settings-container">
    
        <div className="settings-options">
          <div className="settings-option">
          
          </div>
          <div className="settings-option">

            <button className="settings-button">Give Feedback</button>
          </div>
          <div className="settings-option">

            <button className="settings-button">Logout</button>
          </div>
        </div>
      </div>
    );
  };
  
  export default Settings;