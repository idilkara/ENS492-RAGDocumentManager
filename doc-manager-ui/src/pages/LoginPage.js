import React from 'react';
import { useNavigate } from 'react-router-dom';
import './LoginPage.css'; // Add styles if needed

const Login = () => {
    const navigate = useNavigate();

    const handleLogin = () => {
        // Here you would integrate CAS authentication
        // For now, just redirect to the Main UI
        navigate('/main');
    };

    return (
        <div className="login-container">

<div className="login-mini-container">
            <h1>Welcome to Sabancı University Document Manager</h1>
            <button className="login-button" onClick={handleLogin}>Login via CAS</button>
        </div></div>
    );
};

export default Login;
