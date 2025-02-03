import React, { useState, useEffect } from 'react';
import './Main.css';
import SidePanel from './sidepanel'; // Import the SidePanel component
import ChatbotUI from './chatbot'; // Import the ChatbotUI component

const Main = () => {
  const [chatID, setChatID] = useState(null);
  const [sessions, setSessions] = useState([]);
  const [chats, setChats] = useState({});

  useEffect(() => {
      // Fetch user sessions when the component mounts
      fetchUserSessions();
  }, []);

  useEffect(() => {
    console.log("🔍 Chat ID Updated:", chatID);
}, [chatID]);


const fetchUserSessions = async () => {
    try {
        console.log("🔄 Fetching user sessions...");
        const response = await fetch('http://localhost/api/get_user_sessions?user_id=1',  {mode:'cors'});
        const data = await response.json();
        console.log("✅ User sessions fetched:", data);

        setSessions(data);
        if (data.length > 0) {
            const firstSessionId = data[0].session_id;
            console.log("📌 Setting initial Chat ID:", firstSessionId);
            setChatID(firstSessionId);

            // Immediately fetch the chat history for the first session
            await fetchChatSession(firstSessionId);
        } else {
            console.log("⚠️ No sessions found, user needs to create a new chat.");
        }
    } catch (error) {
        console.error("❌ Error fetching user sessions:", error);
    }
};


  const handleChatIDChange = async (newChatID) => {
      if (newChatID === "NONE") {
          await createNewChatSession();
      } else {
          setChatID(newChatID);
          await fetchChatSession(newChatID);
      }
  };
  const createNewChatSession = async () => {
    try {
        console.log("➕ Creating a new chat session...");
        const response = await fetch('http://localhost/api/create_chat_session', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ user_id: '1' }),
        });
        const data = await response.json();
        console.log("✅ New chat session created:", data);

        const newSession = { 
            user_id: '1', 
            session_id: data.session_id, 
            created_at: new Date().toISOString() 
        };
        setSessions([...sessions, newSession]);

        console.log("📌 Setting new Chat ID:", data.session_id);
        setChatID(data.session_id);
        setChats(prev => ({ ...prev, [data.session_id]: [] }));
    } catch (error) {
        console.error("❌ Error creating new chat session:", error);
    }
};


  const fetchChatSession = async (sessionID) => {
    try {
        console.log(`🔄 Fetching chat session for session_id: ${sessionID}`);
        const response = await fetch(`http://localhost/api/get_chat_session?user_id=1&session_id=${sessionID}`);
        const data = await response.json();
        console.log(`✅ Chat history for session_id=${sessionID}:`, data);

        // Convert backend conversation to frontend message format
        const formattedMessages = data.map((msg, index) => [
            { id: index * 2, text: msg.user_query, isBot: false },
            { id: index * 2 + 1, text: msg.agent_response, isBot: true }
        ]).flat();

        // Update chats state
        setChats(prev => ({ ...prev, [sessionID]: formattedMessages }));
    } catch (error) {
        console.error("❌ Error fetching chat session:", error);
        setChats(prev => ({ ...prev, [sessionID]: [] }));
    }
};


  return (
      <div className="main-container">
          <div className="left-panel">
              <SidePanel 
                  chatID={chatID} 
                  setChatID={handleChatIDChange} 
                  sessions={sessions} 
              />
          </div>
          <div className="right-panel">
              <ChatbotUI chatID={chatID} chats={chats} />
          </div>
      </div>
  );
};

export default Main;


