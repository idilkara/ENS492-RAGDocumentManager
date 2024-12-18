import React, { useState, useRef, useEffect } from "react";
import ReactMarkdown from "react-markdown";
import './chatbot.css';
import axios from 'axios';

const ChatbotUI = ({ chatID, chats }) => {
  /*const [messages, setMessages] = useState([
    { id: 1, text: 'Hello! How can I assist you today?', isBot: true },
  ]); */
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState(chats[chatID]);

  const chatHistoryRef = useRef(null); // Create a reference for the chat container


  const handleSendMessage = async () => {
    if (input.trim() === "") return;
    
    const userMessage = { id: Date.now(), text: input, isBot: false };
    setMessages((prev) => [...prev, userMessage]);
    try {
      const response = await axios.post("http://127.0.0.1:5000/user_query", {
        query: input
      });

      const data = response.data;
      // console.log(response.data)
      // const data =  `  
      // ${response.data}
      // `;

      const botResponse = typeof data.response === 'string' ? data.response : JSON.stringify(data.response);
      const filePath = data.file_path || null;

      // Ensure file path is handled separately
      setMessages((prev) => [
        ...prev,
        {
          id: Date.now() + 1,
          text: botResponse,  // Only response, no file path in text
          isBot: true,
          filePath: filePath, // Store filePath separately for the "View PDF" button
        },
      ]);


    } catch (error) {
      console.error("Error sending request:", error);
      setMessages((prev) => [
        ...prev,
        { id: Date.now() + 1, text: "Sorry, there was an issue processing your request.", isBot: true },
      ]);
    }

    setInput("");
  };

  const handleViewPDFClick = async (filePath) => {
    if (!filePath) return;

    try {
      const response = await axios.get(`http://127.0.0.1:5000/get_pdf?file_path=${encodeURIComponent(filePath)}`, {
        responseType: 'blob',
      });

      const blob = new Blob([response.data], { type: 'application/pdf' });
      const url = window.URL.createObjectURL(blob);

      // Open the PDF in a new tab
      window.open(url, "_blank");
    } catch (error) {
      console.error("Error fetching PDF:", error);
    }
  };



  // Scroll to the most recent message
  /*
  useEffect(() => {
    if (chatHistoryRef.current) {
      chatHistoryRef.current.scrollTop = chatHistoryRef.current.scrollHeight;
    }
  }, [messages]); // Triggered whenever messages are updated
*/
useEffect(() => {
    setMessages(chats[chatID]);
  }, [chatID, chats]);
    

  return (
    <div className="chat-interaction-container">

      <div className="chat-container">
        {/*<div className="chat-header"><h2>SUDoc</h2></div> */}

        <div className="chat-history">
          {messages.map((msg) => (
            <div key={msg.id} className={`message ${msg.isBot ? 'bot' : 'user'}`}>
             <ReactMarkdown>{msg.text}</ReactMarkdown> 

              {/* Show the button below the chatbot message only if filePath exists */}
              {msg.isBot && msg.filePath && (
                <button className="display-button" onClick={() => handleViewPDFClick(msg.filePath)}>
                  <div className= "pdfLabel">View PDF</div >
                </button>
              )}
            </div>
          ))}
        </div>

        <div className="input-container">

          <textarea
            
            type="text"
            className="text-input"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Type your message..."
          />
          <button className="send-button" onClick={handleSendMessage}>
            Send
          </button>

    
        </div>
        <div className="feedback-link">Give us feedback!</div>


      </div>
    </div>
  );
};

export default ChatbotUI;
