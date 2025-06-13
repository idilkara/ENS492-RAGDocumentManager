import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './LoginPage.css';
import config from "../config";

const Login = () => {
    const navigate = useNavigate();

    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');
    const [error, setError] = useState('');
    const [isRegistering, setIsRegistering] = useState(false);

    const handleLogin = async () => {
        setError('');

        try {
            const response = await fetch(`${config.API_BASE_URL}/login`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({email, password})
            });

            const data = await response.json();

            if(response.ok) {
                localStorage.setItem('authToken', data.token);
                localStorage.setItem('userRole', data.role);
                localStorage.setItem("userId", data.user_id);
                navigate('/main');
            } else {
                setError(data.message || 'Login failed, please try again.');
            }
        }
        catch(error) {
            setError('An error occurred when trying to log in. Please try again later.');
            console.error('Login error: ', error);
        }
    };

    const handleCAS = () => {
        // Redirect to the CAS landing page
        window.location.href = `${config.API_BASE_URL}/cas-login`;
        // Note: The CAS landing page should handle the authentication flow
        // and redirect back to the main application with the necessary tokens.
    }

    const handleRegister = async () => {
        setError('');
        
        // Basic validation
        if (!email || !password) {
            setError('Please enter both email and password.');
            return;
        }
        
        if (password !== confirmPassword) {
            setError('Passwords do not match.');
            return;
        }

        try {
            const response = await fetch(`${config.API_BASE_URL}/register`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({email, password})
            });

            const data = await response.json();

            if(response.ok) {
                // Switch back to login view on successful registration
                setIsRegistering(false);
                setEmail('');
                setPassword('');
                setConfirmPassword('');
                // You could also add a success message here
                alert('Registration successful! Please login with your new credentials.');
            } else {
                setError(data.message || 'Registration failed, please try again.');
            }
        }
        catch(error) {
            setError('An error occurred during registration. Please try again later.');
            console.error('Registration error: ', error);
        }
    };

    const toggleRegisterView = () => {
        setIsRegistering(!isRegistering);
        setEmail('');
        setPassword('');
        setConfirmPassword('');
        setError('');
    };

    return (
        <div className="login-container">
            <div className="login-mini-container">
                <h1>Welcome to Sabancı University Document Manager</h1>
                
                {/*!isRegistering ? (
                    // Login View
                    <>
                        <input
                            type="email"
                            placeholder="Enter your email"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            className="login-input"
                        />
                        <input
                            type="password"
                            placeholder="Enter your password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            className="login-input"
                        />
                        <button className="login-button" onClick={handleLogin}>Login</button>
                        <button className="login-button" onClick={toggleRegisterView}>Register</button>
                    </>
                ) : (
                    // Register View
                    <>
                        <input
                            type="email"
                            placeholder="Enter your email"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            className="login-input"
                        />
                        <input
                            type="password"
                            placeholder="Create password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            className="login-input"
                        />
                        <input
                            type="password"
                            placeholder="Confirm password"
                            value={confirmPassword}
                            onChange={(e) => setConfirmPassword(e.target.value)}
                            className="login-input"
                        />
                        <button className="login-button" onClick={handleRegister}>Create Account</button>
                        <button className="login-button" onClick={toggleRegisterView}>Back to Login</button>
                    </>
                )*/}
                <button className="login-button" onClick={handleCAS}>Login with CAS</button>
                {error && <div className="login-error">{error}</div>}
            </div>
        </div>
    );
};

export default Login;