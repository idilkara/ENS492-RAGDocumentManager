// App.js
import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Main from './pages/Main'; // Adjust the path if your `main.js` is located elsewhere
import './root.css';

const App = () => {
  return (
    <Router>
      <Routes>
        {/* Route to the main chatbot UI */}
        <Route path="/" element={<Main />} />
      </Routes>
    </Router>
  );
};

export default App;
