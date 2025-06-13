// src/pages/CASLanding.js
import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

const CASLanding = () => {
  const navigate = useNavigate();

  useEffect(() => {
    const query = new URLSearchParams(window.location.search);
    const token = query.get("token");
    const role = query.get("role");
    const user_id = query.get("user_id");

    if (token && role && user_id) {
      localStorage.setItem("authToken", token);
      localStorage.setItem("userRole", role);
      localStorage.setItem("userId", user_id);
      navigate("/main"); // Auth complete, go to app
    } else {
      console.error("Missing token or user data in URL");
      navigate("/login?error=missing_token");
    }
  }, [navigate]);

  return <div>Logging you in...</div>;
};

export default CASLanding;
