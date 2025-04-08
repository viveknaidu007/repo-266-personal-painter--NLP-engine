import React, { useState } from 'react';
import axios from 'axios';
import './ChatWindow.css';

const ChatWindow = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [prompt, setPrompt] = useState('');

  const sendMessage = async () => {
    if (!input.trim()) return;
    setMessages([...messages, { text: input, sender: 'user' }]);
    try {
      console.log('Sending request to /api/chat with:', { message: input });
      const response = await axios.post('http://localhost:8000/api/chat', { message: input }, {
        headers: { 'Content-Type': 'application/json' }
      });
      console.log('Response received:', response.data);
      setPrompt(response.data.prompt || 'No prompt generated');
    } catch (error) {
      console.error('Error:', error.message, error.response?.data);
      setPrompt(`Error: ${error.message}`);
    }
    setInput('');
  };

  const resetChat = async () => {
    await axios.get('/api/chat/reset-chat');
    setMessages([]);
    setPrompt('');
  };

  return (
    <div className="chat-container">
      <h2>Personal Painter Chat</h2>
      <div className="messages">
        {messages.map((msg, idx) => (
          <div key={idx} className={msg.sender}>{msg.text}</div>
        ))}
      </div>
      <input
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
        placeholder="Talk about your feelings or ideas..."
      />
      <button onClick={sendMessage}>Send</button>
      <button onClick={resetChat}>Reset</button>
      <div className="response-area">
        <h3>Generated Prompt:</h3>
        <div className="response">{prompt || 'Waiting for response...'}</div>
      </div>
    </div>
  );
};

export default ChatWindow;