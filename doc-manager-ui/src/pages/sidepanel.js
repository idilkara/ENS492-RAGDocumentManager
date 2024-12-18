import React, { useState, useEffect } from 'react';
import './sidepanel.css';
import Settings from './side-panel-options/sidepanelSettings'; // Import the Settings component
import FileUpload from './side-panel-options/sidepanelupload'; // Import the Settings component
import SUlogo from '../assets/Sabanci_University_logo.png';
import Search from './side-panel-options/sidepanelsearch'; // Import the Settings component
import DeleteIcon from "../assets/chat-circle-remove-svgrepo-com.svg"
import CreateIcon from "../assets/chat-circle-add-svgrepo-com.svg"
import ChatsIcon from "../assets/chat-conversation-circle-svgrepo-com.svg"
import SettingsIcon from "../assets/settings-svgrepo-com.svg" 
import UploadIcon from "../assets/upload-file-2-svgrepo-com.svg"

const SidePanel = ( { chatID, setChatID } ) => {

  //states 

  const [selectedOption, setSelectedOption] = useState(0);
  const options = ["Chats", "Upload a document", "Settings"];
  const optionIcons = [ChatsIcon, SettingsIcon, UploadIcon];



  const renderListingContent = () => {
    switch (selectedOption) {
      case 0: // Saved chats
        return (

          <div className="side-panel-listing">
          
        <div className="side-panel-listing-createchat"
        onClick={() => setChatID("NONE")}>
          
    
          <div>New Chat</div>
          <img src={CreateIcon} alt="createicon" style={{ width: '20px', height: 'auto' }} />
        </div>

 

            <div className="side-panel-listing-element"
            onClick={() => setChatID("chat1")}>
            <div className="side-panel-listing-element-subtitle-container">
         
                 <div>chat1 </div> <img src={DeleteIcon} alt="deleteicon" style={{ width: '20px', height: 'auto' }}  />
              
              </div>


              <div className="side-panel-listing-element-references">
                <div className="side-panel-listing-element-reference">Document2 ref</div>
                <div className="side-panel-listing-element-reference">Document2 ref2</div>
              </div>
            </div>
            <div className="side-panel-listing-element"
            onClick={() => setChatID("chat2")}>
              
            <div className="side-panel-listing-element-subtitle-container">
                 <div>chat2 </div> <img src={DeleteIcon} alt="deleteicon" style={{ width: '20px', height: 'auto' }}  />
              </div>

              <div className="side-panel-listing-element-references">
                <div className="side-panel-listing-element-reference">Document2 ref</div>
                <div className="side-panel-listing-element-reference">Document2 ref2</div>
                <div className="side-panel-listing-element-reference">Document2 ref23</div>
                <div className="side-panel-listing-element-reference">Document2 ref5</div>
              </div>
            </div>

            <div className="side-panel-listing-element"
            onClick={() => setChatID("chat3")} >
              
            <div className="side-panel-listing-element-subtitle-container">
                 <div>chat3</div> <img src={DeleteIcon} alt="deleteicon" style={{ width: '20px', height: 'auto' }}  />
              </div>

              <div className="side-panel-listing-element-references">
                <div className="side-panel-listing-element-reference">Document2 ref</div>
                <div className="side-panel-listing-element-reference">Document2 ref2</div>
                <div className="side-panel-listing-element-reference">Document2 ref23</div>
                <div className="side-panel-listing-element-reference">Document2 ref5</div>
              </div>
            </div>
            
          </div>
        );
      // case 1: // Settings
      //   return <Search/>; // Render the Settings component
        

      case 2: // Settings
        return <Settings />; // Render the Settings component
        
      case 1: // Settings
        return <FileUpload/>; // Render the Settings component
        
      default:
        return <div className="side-panel-listing">No content available for this option.</div>;
    }
  };




  return (


    <div className="side-panel">
    <div className="side-panel-upper">
      <div className="side-panel-title">

      <div className="logo-container">
            <img src={SUlogo} alt="SUlogo" style={{ width: '150px', height: 'auto' }}  />
        </div> 

      <div className="side-panel-title-text">Document Management System</div>


      </div>


    </div>

  

    <div className="side-panel-lower">
      <div className="side-panel-listing-title">{options[selectedOption]}    </div>
      {renderListingContent()}
    </div>
    <div className="side-panel-bottom">
      <div className="side-panel-options">


        {options.map((option, index) => (
          <div
            key={index}
            className={`side-panel-options-button ${selectedOption === index ? 'active' : ''}`}
            onClick={() => setSelectedOption(index)}
          >
             <img src={optionIcons[index]} alt="deleteicon" style={{ width: '20px', height: 'auto' }}  /> <div>{option}</div>

          </div>
        ))}
      </div>
    </div>
  </div>



  );
};

export default SidePanel;
