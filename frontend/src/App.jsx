import React from 'react';
import ChatWindow from './components/ChatWindow';
import SearchBar from './components/SearchBar';
import './styles.css';

function App() {
  return (
    <div className="app">
      <h1>Personal Painter</h1>
      <ChatWindow />
      <SearchBar />
    </div>
  );
}

export default App;