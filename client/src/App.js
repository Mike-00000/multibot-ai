import './App.css';
import { Box } from '@mui/material'
import DashboardField from './components/DashboardField';
import ChatWindow from './components/ChatWindow';
import Header from './components/Header';
import { ChatProvider } from './components/ChatContext';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';


function App() {
  return (
    <ChatProvider>
      <Router>
        <Header/>
      <Box
        height="88vh"
        display="flex"
        flexDirection="column"
        justifyContent="space-between"
      >
        <Switch>
          <Route path="/:botId">
            <ChatWindow />
            <DashboardField/>
          </Route>
        </Switch>
      </Box>
      </Router>
    </ChatProvider>
    
  );
}

export default App;
