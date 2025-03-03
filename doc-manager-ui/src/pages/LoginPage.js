import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './LoginPage.css'; // Add styles if needed
import config from "../config";

const Login = () => {
    const navigate = useNavigate();

    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');

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

            if(response.ok)
            {
                localStorage.setItem('authToken', data.token);
                localStorage.setItem('userRole', data.role);
                localStorage.setItem("userId", data.user_id)
                navigate('/main');
            } else {
                setError(data.message || 'Login failed, please try again.');
            }
        }
        catch(error) {
            setError('An error occured when trying to log in. Please try again later.');
            console.error('Login error: ', error);
        }
    };

    return (
        <div className="login-container">
            <div className="login-mini-container">
                <h1>Welcome to Sabancı University Document Manager</h1>
                {/* Email Input */}
                <input
                    type="email"
                    placeholder="Enter your email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    className="login-input"
                />

                {/* Password Input */}
                <input
                    type="password"
                    placeholder="Enter your password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    className="login-input"
                />
                <button className="login-button" onClick={handleLogin}>Login via CAS</button>
                {error && <div className="login-error">{error}</div>}
            </div>
        </div>
    );
};

export default Login;
