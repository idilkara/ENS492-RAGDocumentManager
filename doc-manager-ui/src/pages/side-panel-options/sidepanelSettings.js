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
    


            <label className="settings-button">Give Feedback</label>
            <label className="settings-button">Logout</label>
          
   
      </div>
    );
  };
  
  export default Settings;