import React, { createContext, useContext, useState } from 'react';
import axios from 'axios';
import { v4 as uuidv4 } from 'uuid';

const ChatContext = createContext();
export const useChatContext = () => useContext(ChatContext);

export const ChatProvider = ({ children }) => {
  const [chatState, setChatState] = useState({
    messages: [],
  });

    const addMessage = (message) => {
        setChatState((prevState) => {
          const newMessage = {
            ...message,
            id: uuidv4(),
          };

          const newState = {
              ...prevState,
              messages: [...prevState.messages, newMessage],
          };
          return newState;
        });
    };

    const sendMessage = async (message) => {
        addMessage({ content: message, role: 'user' });
      
        try {
          const response = await axios.post(`/api/user_input`, { message });
      
          if (response.status === 200) {
            addMessage({ content: response.data.message, role: 'assistant' });
          }
        } catch (error) {
          console.error('Error sending message:', error);
        }
      };
  
  return (
    <ChatContext.Provider value={{ chatState, addMessage, sendMessage }}>
      {children}
    </ChatContext.Provider>
  );
};
  