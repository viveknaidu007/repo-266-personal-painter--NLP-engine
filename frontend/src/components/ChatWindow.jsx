import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './ChatWindow.css';

const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
const recognition = SpeechRecognition ? new SpeechRecognition() : null;

const ChatWindow = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [prompt, setPrompt] = useState('');
  const [images, setImages] = useState([]);
  const [isListening, setIsListening] = useState(false);
  const [conversation, setConversation] = useState([]);
  const [isMultiTurn, setIsMultiTurn] = useState(false);

  // Initialize SpeechRecognition
  useEffect(() => {
    if (!recognition) {
      console.error('SpeechRecognition API not supported in this browser');
      return;
    }
    recognition.continuous = true; // Allow multi-turn voice input
    recognition.interimResults = false;
    recognition.onresult = (event) => {
      const transcript = event.results[event.results.length - 1][0].transcript;
      setInput(transcript);
      setConversation([...conversation, transcript]);
      console.log('Voice transcribed:', transcript);
    };
    recognition.onerror = (event) => {
      console.error('Speech error:', event.error);
      setIsListening(false);
    };
    recognition.onend = () => {
      if (isListening) {
        recognition.start(); // Restart if still listening
      }
    };
    return () => recognition.stop(); // Cleanup on unmount
  }, [conversation, isListening]);

  const startListening = () => {
    if (recognition && !isListening) {
      recognition.start();
      setIsListening(true);
      console.log('Voice input started');
    } else {
      console.log('Voice input already started or not supported');
    }
  };

  const stopListening = () => {
    if (recognition && isListening) {
      recognition.stop();
      setIsListening(false);
      console.log('Voice input stopped, sending message');
      sendMessage(); // Send transcribed input
    } else {
      console.log('Voice input not active or not supported');
    }
  };

  const sendMessage = async () => {
    if (!input.trim()) return;
    const userMessage = { text: input, sender: 'user' };
    setMessages([...messages, userMessage]);
    setConversation([...conversation, input]);

    if (conversation.length < 2 && !isMultiTurn) {
      setPrompt('Please elaborate more (e.g., describe your feelings, memories, or details) for a richer prompt. Continue chatting!');
      setIsMultiTurn(true);
      return;
    }

    try {
      console.log('Sending request to /api/chat with:', { message: input, conversation });
      const response = await axios.post('http://localhost:8000/api/chat', {
        message: input,
        conversation: conversation
      }, {
        headers: { 'Content-Type': 'application/json' }
      });
      console.log('Response received:', response.data);
      setPrompt(response.data.prompt || 'No prompt generated');
      setImages(response.data.images || []);
      setIsMultiTurn(false);
    } catch (error) {
      console.error('Error:', error.message, error.response?.data);
      setPrompt(`Error: ${error.message}`);
    }
    setInput('');
  };

  const resetChat = async () => {
    await axios.get('http://localhost:8000/api/chat/reset-chat');
    setMessages([]);
    setPrompt('');
    setImages([]);
    setConversation([]);
    setIsMultiTurn(false);
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
      <button onClick={startListening} disabled={isListening}>Start Voice</button>
      <button onClick={stopListening} disabled={!isListening}>Stop Voice</button>
      <button onClick={resetChat}>Reset</button>
      <div className="response-area">
        <h3>Generated Prompt:</h3>
        <div className="response">{prompt || 'Waiting for response...'}</div>
      </div>
      <div className="image-gallery">
        <h3>Generated Images:</h3>
        {images.length > 0 ? (
          images.map((img, idx) => (
            <img
              key={idx}
              src={`data:image/jpeg;base64,${img}`}
              alt={`Generated ${idx + 1}`}
              width="200"
            />
          ))
        ) : (
          <p>No images generated yet.</p>
        )}
      </div>
    </div>
  );
};

export default ChatWindow;