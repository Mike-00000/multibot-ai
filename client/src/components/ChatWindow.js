import { Box, Stack, Paper, Button } from '@mui/material'
import { ThemeProvider, useTheme  } from '@mui/material/styles';
import { useState, useEffect } from 'react'
import { styled } from '@mui/material/styles'
import { useChatContext } from './ChatContext';
import { useParams } from 'react-router-dom';

const ChatWindow = ({}) => {
    // const { botId } = useParams();
    // console.log("ChatWindow for bot with ID:", botId);
    const [message, setMessage] = useState('');
    // const [start, setStart] = useState(0); 
    // const [end, setEnd] = useState(10);  

    const { chatState, addMessage, sendMessage } = useChatContext();
    const history = chatState.messages;
    const theme = useTheme();

    const handleSendMessage = () => {
      sendMessage(message);
      setMessage('');
    };

    // useEffect(() => {
    //   if (isAtBottomOfChatHistory()) {
    //     loadMoreMessages();
    //   }
    // }, [chatState]);
    

    const UserItem = ({ message, theme }) => {
      return (
        <ThemeProvider theme={theme}>
          <Paper key={message.id} style={{ backgroundColor: 'rgb(56, 116, 203)', 
            ...theme.typography.body2,
            padding: theme.spacing(1),
            textAlign: 'right',
            color: 'white',
            maxWidth: '70%' }}>
              {message.content}
          </Paper>
        </ThemeProvider>
      );
    };
    

    const BotItem = ({ theme, message }) => (
      <ThemeProvider theme={theme}>
        <Paper
          key={message.id}
          style={{
            backgroundColor: 'rgb(221, 221, 221)',
            ...theme.typography.body2,
            padding: theme.spacing(1),
            textAlign: 'left',
            color: 'black',
            maxWidth: '70%',
          }}
        >
          {message.content}
        </Paper>
      </ThemeProvider>
    );
    
    

    // useEffect(() => {

    // }, [botId, start, end, addMessage]);
    
    // const handleTestMessage = () => {
    //   addMessage({ content: "Message test", role: 'user' });
    // };

    return (
      <Box>
        {history.map((message) => (
          <div key={message.id} style={{ width: '80%', display: 'flex', justifyContent: message.role === 'user' ? 'flex-end' : 'flex-start' }}>
            {message.role === 'user' && (
              <UserItem message={message} theme={theme} />
            )}
            {message.role === 'assistant' && (
              <BotItem message={message} theme={theme} />
            )}
          </div>
        ))}
      </Box>
    )
}

export default ChatWindow;
