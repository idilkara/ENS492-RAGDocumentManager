import React, { useState } from 'react';
import './sidepanelsearch.css'; // Import the CSS file for styling
import config from "../../config";

const SearchDocument = () => {
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState([]);
  const [isSearching, setIsSearching] = useState(false);

  const handleSearch = async () => {
    if (!searchQuery.trim()) return; // Prevent empty searches

    setIsSearching(true);
    try {
      const token = localStorage.getItem("authToken");
      const response = await fetch(`${config.API_BASE_URL}/search?query=${encodeURIComponent(searchQuery)}`, {
        method: 'GET',
        headers: {'Authorization': `Bearer ${token}`},
      });

      const result = await response.json();
      console.log('Search result:', result);

      if (response.ok) {
        setSearchResults(result.documents || []); // Assume the response includes a "documents" field
      } else {
        setSearchResults([]);
        alert(result.error || 'Error fetching search results');
      }
    } catch (error) {
      console.error('Error searching documents:', error);
      setSearchResults([]);
      alert('Failed to perform search');
    } finally {
      setIsSearching(false);
    }
  };

  return (
    <div className="search-container">

      <div className="search-bar">
        
        <input
          type="text"
          className="search-input"
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          placeholder="Enter document title or keyword"
        />


        <button className="search-button" onClick={handleSearch} disabled={isSearching}>
          {isSearching ? 'Searching...' : 'Search'}
        </button>

        
      </div>

      {/* Display search results */}
      <div className="search-results">
        {searchResults.length > 0 ? (
          searchResults.map((doc, index) => (
            <div key={index} className="search-result-item">
              {doc.title || `Document ${index + 1}`}
            </div>
          ))
        ) : (
          <p className="no-results">No results found</p>
        )}
      </div>
    </div>
  );
};

export default SearchDocument;
