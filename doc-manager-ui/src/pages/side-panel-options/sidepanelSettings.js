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
        <h2 className="settings-title">Settings</h2>
        <div className="settings-options">
          <div className="settings-option">
          
            <button className="dark-light-mode-toggle" >
              Switch to {theme === 'Light' ? 'Dark' : 'Light'} Mode
            </button>
          </div>
          <div className="settings-option">

            <button className="feedback-button">Give Feedback</button>
          </div>
          <div className="settings-option">

            <button className="logout-button">Logout</button>
          </div>
        </div>
      </div>
    );
  };
  
  export default Settings;