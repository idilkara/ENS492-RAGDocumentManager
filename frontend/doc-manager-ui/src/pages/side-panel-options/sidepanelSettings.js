import React from 'react';
import { useNavigate } from 'react-router-dom';
import './sidepanelsettings.css';
import config from "../../config";

const Settings = () => {
    const navigate = useNavigate();

    const handleFeedback = () => {
        window.open("https://docs.google.com/forms/d/e/1FAIpQLSedQob3XPLOoiyA3sLy7jsVG0L3twcE_upSVL7ezV7NSuSVYQ/viewform?usp=header", "_blank"); // Opens feedback link in a new tab
    };

    const handleLogout = () => {
        navigate('/'); // Redirects to the login page
    };

    return (
        <div className="settings-container">
            <label className="settings-button" onClick={handleFeedback}>Give Feedback</label>
            <label n className="settings-button" onClick={handleLogout}>Logout</label >
        </div>
    );
};

export default Settings;

  
    // const toggleTheme = () => {
    //   setTheme(theme === 'Light' ? 'Dark' : 'Light');
    //   document.body.className = theme === 'Light' ? 'dark-mode' : 'light-mode'; // Dynamically update the body class
    // };
  
