import React, { useState } from 'react';
import axios from 'axios';
import './SearchBar.css';  // New CSS file

const SearchBar = () => {
  const [query, setQuery] = useState('');
  const [searchType, setSearchType] = useState('image');
  const [results, setResults] = useState([]);

  const performSearch = async () => {
    if (!query.trim()) return;
    const response = await axios.post('/api/search', { query, search_type: searchType });
    setResults(response.data.results);
  };

  return (
    <div className="search-container">
      <h2>Search Paintings</h2>
      <input
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        onKeyPress={(e) => e.key === 'Enter' && performSearch()}
        placeholder="Describe what you want to see..."
      />
      <select value={searchType} onChange={(e) => setSearchType(e.target.value)}>
        <option value="image">Individual Images</option>
        <option value="collection">Collections</option>
      </select>
      <button onClick={performSearch}>Search</button>
      {results.length > 0 && (
        <div className="response">
          <h3>Results:</h3>
          <ul>
            {results.map((result, idx) => (
              <li key={idx}>
                {searchType === 'image' ? (
                  `${result.description} (Score: ${result.score.toFixed(2)})`
                ) : (
                  `Collection ${result.collection_id} (Avg Score: ${result.avg_score.toFixed(2)})`
                )}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default SearchBar;