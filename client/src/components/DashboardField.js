import React, { useState } from "react";
import { TextField, Button, Stack, Tooltip, Box } from "@mui/material";
import Send from '@mui/icons-material/Send';
import { useChatContext } from './ChatContext';
import { useParams } from 'react-router-dom';

const DashboardField = () => {
    const [newMessage, setNewMessage] = useState("");
    const { sendMessage } = useChatContext();

    const handleSendMessage = async () => {
        if (newMessage.trim()) {
            sendMessage(newMessage); 
            setNewMessage(""); 
        }
    };

    return (
        <Box
            display="flex" 
            justifyContent="center" 
        >
            <Stack
                 sx={{
                    width: { xs: '100%', md: '80%' },
                  }}
                direction="row"
                marginBottom={5}
            >
                <TextField
                    multiline
                    value={newMessage}
                    onChange={(e) => {
                        setNewMessage(e.target.value)
                    }}
                    placeholder="Ask something..."
                    fullWidth
                    variant="outlined"
                    onKeyDown={(e) => {
                        if (e.key === 'Enter' && newMessage.trim().length > 0) {
                            handleSendMessage();
                            e.preventDefault();
                        }
                    }}
                    sx={{
                        backgroundColor: 'white',
                        lineHeight: '20px',
                        maxHeight: '150px',
                        overflowY: 'auto',
                    }}
                />
                <Tooltip title="Send" placement="top">
                    <span>
                        <Button
                            variant="contained"
                            color="primary"
                            onClick={handleSendMessage}
                            disabled={!newMessage || newMessage.trim().length === 0}
                            sx={{
                                height: '56px',
                                marginLeft: 1,
                                textTransform: 'none',
                            }}
                        >
                            <Stack direction="row" alignItems="center">
                                <Send
                                    sx={{
                                        marginRight: { md: 1 },
                                        color: 'white',
                                    }}
                                />
                                <Box
                                    display={{
                                        xs: 'none',
                                        md: 'block',
                                    }}
                                >
                                    Send
                                </Box>
                            </Stack>
                        </Button>
                    </span>
                    
                </Tooltip>
            </Stack>
        </Box>
    );
};

export default DashboardField;
