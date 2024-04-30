import React from 'react';
import { AppBar, Toolbar, Typography, Box } from '@mui/material';
import mathTutor from './mtutor.png';

const Header = () => {
  return (
    <AppBar position="static" sx={{ bgcolor: 'black' }}>
      <Toolbar>
        <Box
          component="img"
          sx={{
            borderRadius: '50%', overflow: 'hidden',
            height: 50, 
            width: 50, 
            padding: 2
          }}
          alt="Math Tutor"
          src={mathTutor} 
        />
        <Typography variant="h6" color="inherit">
          Math Tutor
        </Typography>
      </Toolbar>
    </AppBar>
  );
};

export default Header;