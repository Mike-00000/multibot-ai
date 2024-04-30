import React, { createContext, useContext, useState } from 'react'

const ConversationContext = createContext()

export const ConversationProvider = ({ children }) => {
  const [userConversations, setUserConversations] = useState([])

  const addConversation = (Conversation) => {
    setUserConversations([...userConversations, Conversation])
  }

  return (
    <ConversationContext.Provider value={{ userConversations, addConversation }}>
      {children}
    </ConversationContext.Provider>
  )
}

export default ConversationProvider;
