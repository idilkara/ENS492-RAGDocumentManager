import React, { useState, useEffect } from 'react';
import './sidepanel.css';
import Settings from './side-panel-options/sidepanelSettings'; // Import the Settings component
import FileUpload from './side-panel-options/sidepanelupload'; // Import the Settings component

import Search from './side-panel-options/sidepanelsearch'; // Import the Settings component

const SidePanel = ( ) => {

  //states 

  const [selectedOption, setSelectedOption] = useState(0);
  const options = ["Chats", "Search for a document", "Upload a document", "Settings"];



  const renderListingContent = () => {
    switch (selectedOption) {
      case 0: // Saved chats
        return (

          <div className="side-panel-listing">
            <div className="side-panel-listing-element">new chat </div> 

            <div className="side-panel-listing-element">chat 1
              <div className="side-panel-listing-element-references">
                <div className="side-panel-listing-element-reference">Document2 ref</div>
                <div className="side-panel-listing-element-reference">Document2 ref2</div>
              </div>
            </div>
            <div className="side-panel-listing-element">chat 2
              <div className="side-panel-listing-element-references">
                <div className="side-panel-listing-element-reference">Document2 ref</div>
                <div className="side-panel-listing-element-reference">Document2 ref2</div>
                <div className="side-panel-listing-element-reference">Document2 ref23</div>
                <div className="side-panel-listing-element-reference">Document2 ref5</div>
              </div>
            </div>

            <div className="side-panel-listing-element">chat 2
              <div className="side-panel-listing-element-references">
                <div className="side-panel-listing-element-reference">Document2 ref</div>
                <div className="side-panel-listing-element-reference">Document2 ref2</div>
                <div className="side-panel-listing-element-reference">Document2 ref23</div>
                <div className="side-panel-listing-element-reference">Document2 ref5</div>
              </div>
            </div>
            <div className="side-panel-listing-element">chat 2
              <div className="side-panel-listing-element-references">
                <div className="side-panel-listing-element-reference">Document2 ref</div>
                <div className="side-panel-listing-element-reference">Document2 ref2</div>
                <div className="side-panel-listing-element-reference">Document2 ref23</div>
                <div className="side-panel-listing-element-reference">Document2 ref5</div>
              </div>
            </div>
            <div className="side-panel-listing-element">chat 2
              <div className="side-panel-listing-element-references">
                <div className="side-panel-listing-element-reference">Document2 ref</div>
                <div className="side-panel-listing-element-reference">Document2 ref2</div>
                <div className="side-panel-listing-element-reference">Document2 ref23</div>
                <div className="side-panel-listing-element-reference">Document2 ref5</div>
              </div>
            </div>
            <div className="side-panel-listing-element">chat 2
              <div className="side-panel-listing-element-references">
                <div className="side-panel-listing-element-reference">Document2 ref</div>
                <div className="side-panel-listing-element-reference">Document2 ref2</div>
                <div className="side-panel-listing-element-reference">Document2 ref23</div>
                <div className="side-panel-listing-element-reference">Document2 ref5</div>
              </div>
            </div>
          </div>
        );
      case 1: // Settings
        return <Search/>; // Render the Settings component
        

      case 3: // Settings
        return <Settings />; // Render the Settings component
        
      case 2: // Settings
        return <FileUpload/>; // Render the Settings component
        
      default:
        return <div className="side-panel-listing">No content available for this option.</div>;
    }
  };




  return (


    <div className="side-panel">
    <div className="side-panel-upper">
      <div className="side-panel-title">Sabancı University Document Management System</div>

      <hr />
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
            {option}
          </div>
        ))}
      </div>
    </div>
  </div>



  );
};

export default SidePanel;
