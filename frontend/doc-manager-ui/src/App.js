import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Login from './pages/LoginPage'; // Import the Login page
import Main from './pages/Main'; // Import the Main UI
import CASLanding from './pages/CASLanding'; // Import the CAS Landing page
import './root.css';

const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Login />} /> {/* Default route -> Login */}
        <Route path="/cas-landing" element={<CASLanding />} />
        <Route path="/main" element={<Main />} /> {/* Chatbot UI */}
      </Routes>
    </Router>
  );
};

export default App;
