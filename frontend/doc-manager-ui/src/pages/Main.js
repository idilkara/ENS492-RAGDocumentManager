import React, { useState, useEffect } from 'react';
import './Main.css';
import SidePanel from './sidepanel'; // Import the SidePanel component
import ChatbotUI from './chatbot'; // Import the ChatbotUI component
import config from "../config";

import DocumentManagement from './documentManagement.js'


const Main = () => {
  const [chatID, setChatID] = useState(null);
  const [sessions, setSessions] = useState([]);
  const [chats, setChats] = useState({});
  const [selectedOption, setSelectedOption] = useState(0);


  useEffect(() => {
      // Fetch user sessions when the component mounts
      fetchUserSessions();
  }, []);

    useEffect(() => {
        fetchUserSessions();
    }, [chatID, chats]);
  

  const fetchUserSessions = async () => {
      try {
        const response = await fetch(`${config.API_BASE_URL}/get_user_sessions?user_id=1`);
          const data = await response.json();
          setSessions(data);
          
          if (chatID > 0) {
              //const firstSessionId = data[0].session_id;
              setChatID(chatID);
              
              // Immediately fetch the chat history for the first session
              await fetchChatSession(chatID);
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

  const renderRightPanel = () => {
    switch (selectedOption) {
      case 0:
        return <ChatbotUI chatID={chatID} chats={chats} fetchUserSessions={fetchUserSessions} />;
      case 1:
        return <DocumentManagement />;
      case 2:
        return <ChatbotUI chatID={chatID} chats={chats} fetchUserSessions={fetchUserSessions} />;
      default:
        return <ChatbotUI chatID={chatID} chats={chats} fetchUserSessions={fetchUserSessions} />;
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

                  selectedOption={selectedOption}
                  setSelectedOption={setSelectedOption} // Pass state setter to SidePanel

              />
          </div>
          <div className="right-panel">
              {renderRightPanel()} 
          </div>
      </div>
  );
};

export default Main;