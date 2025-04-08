import React, { useState } from 'react';
import axios from 'axios';

const ChatWindow = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [prompt, setPrompt] = useState('');
  const [images, setImages] = useState([]);

  const sendMessage = async () => {
    if (!input.trim()) return;
    setMessages([...messages, { text: input, sender: 'user' }]);
    const response = await axios.post('/api/chat', { message: input });
    setPrompt(response.data.prompt);
    setImages(response.data.images);
    setInput('');
  };

  const resetChat = async () => {
    await axios.get('/api/chat/reset-chat');
    setMessages([]);
    setPrompt('');
    setImages([]);
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
      {prompt && (
        <div>
          <h3>Generated Prompt:</h3>
          <p>{prompt}</p>
        </div>
      )}
      {images.length > 0 && (
        <div>
          <h3>Generated Images:</h3>
          <ul>
            {images.map((img, idx) => (
              <li key={idx}>{img}</li> // Replace with <img> if real URLs
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default ChatWindow;