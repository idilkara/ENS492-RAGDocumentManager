import React, { useState, useEffect } from 'react';
import './Main.css';
import SidePanel from './sidepanel'; // Import the SidePanel component
import ChatbotUI from './chatbot'; // Import the ChatbotUI component
import config from "../config";


const Main = () => {
  const [chatID, setChatID] = useState(null);
  const [sessions, setSessions] = useState([]);
  const [chats, setChats] = useState({});

  useEffect(() => {
      // Fetch user sessions when the component mounts
      fetchUserSessions();
  }, []);

  const fetchUserSessions = async () => {
      try {
        const response = await fetch(`${config.API_BASE_URL}/get_user_sessions?user_id=1`);
          const data = await response.json();
          setSessions(data);
          
          if (data.length > 0) {
              const firstSessionId = data[0].session_id;
              setChatID(firstSessionId);
              
              // Immediately fetch the chat history for the first session
              await fetchChatSession(firstSessionId);
          }
      } catch (error) {
          console.error('Error fetching user sessions:', error);
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
          const response = await fetch(`${config.API_BASE_URL}/create_chat_session`, {
              method: 'POST',
              headers: {
                  'Content-Type': 'application/json',
              },
              body: JSON.stringify({ user_id: '1' }),
          });
          const data = await response.json();
          
          // Update sessions list
          const newSession = { 
              user_id: '1', 
              session_id: data.session_id, 
              created_at: new Date().toISOString() 
          };
          setSessions([...sessions, newSession]);
          
          // Set the new chat ID and initialize its chat history
          setChatID(data.session_id);
          setChats(prev => ({ ...prev, [data.session_id]: [] }));
      } catch (error) {
          console.error('Error creating new chat session:', error);
      }
  };

  const fetchChatSession = async (sessionID) => {
      try {
          const response = await fetch(`${config.API_BASE_URL}/get_chat_session?user_id=1&session_id=${sessionID}`);
          const data = await response.json();
          
          // Convert backend conversation to frontend message format
          const formattedMessages = data.map((msg, index) => [
              { 
                  id: index * 2, 
                  text: msg.user_query, 
                  isBot: false 
              },
              { 
                  id: index * 2 + 1, 
                  text: msg.agent_response, 
                  isBot: true 
              }
          ]).flat();

          // Update chats state with formatted messages
          setChats(prev => ({ ...prev, [sessionID]: formattedMessages }));
      } catch (error) {
          console.error('Error fetching chat session:', error);
          // Ensure an empty array is set if fetch fails
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
                  fetchUserSessions={fetchUserSessions}
              />
          </div>
          <div className="right-panel">
              <ChatbotUI chatID={chatID} chats={chats} />
          </div>
      </div>
  );
};

export default Main;
