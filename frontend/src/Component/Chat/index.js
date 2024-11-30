import React, { useState } from 'react';
import { Box, TextField, Typography, Paper, CircularProgress, IconButton } from '@mui/material';
import { Send } from '@mui/icons-material';
import axios from 'axios';

const ChatInterface = () => {
    const [message, setMessage] = useState('');
    const [chatHistory, setChatHistory] = useState([]);
    const [loading, setLoading] = useState(false);

    const generateSessionId = () => {
        return Math.random().toString(36).substring(2); 
    };
    
    const sessionId = generateSessionId();


    // Handle message input change
    const handleMessageChange = (e) => {
        setMessage(e.target.value);
    };

    // Handle message submission
    const handleSendMessage = async () => {
        if (message.trim()) {
            setChatHistory((prev) => [
                ...prev,
                { text: message, isUser: true },
            ]);
            setMessage(''); 
            setLoading(true); 
    
            try {
                const formData = new FormData();
                formData.append('query', message);
                formData.append('session_id', sessionId);
    

                // Call the backend API to get the response
                const response = await axios.post('http://localhost:8000/api/chat/', formData, {
                    headers: {
                        'Content-Type': 'multipart/form-data',
                    },
                });
    
                // Extract answer and sources from the API response
                const { answer } = response.data;
    
                // Add the assistant's response to the chat history
                setChatHistory((prev) => [
                    ...prev,
                    { text: answer, isUser: false },
                    // ...(source1 ? [{ text: `Source 1: ${source1}`, isUser: false }] : []),
                    // ...(source2 ? [{ text: `Source 2: ${source2}`, isUser: false }] : []),
                    // ...(source3 ? [{ text: `Source 3: ${source3}`, isUser: false }] : []),
                ]);
                setLoading(false);
            } catch (error) {
                setLoading(false);
                // Handle error (e.g., show an error message)
                console.error('Error fetching API response:', error);
                setChatHistory((prev) => [
                    ...prev,
                    { text: error?.response.data.error, isUser: false },
                ]);
            }
        }
    };
    
    const handleKeyDown = (e) => {
        if (e.key === 'Enter' && message.trim()) {
            e.preventDefault();  
            handleSendMessage(); 
        }
    };

    return (
        <Box
            sx={{
                display: 'flex',
                flexDirection: 'column',
                height: '100%',
                marginLeft: 2,
                backgroundColor: '#f5f5f5',
            }}
        >
            {/* Chat History Area */}
            <Box
                sx={{
                    flex: 1,
                    overflowY: 'auto',
                    padding: 2,
                    backgroundColor: '#fff',
                    display: 'flex',
                    textAlign: 'left',
                    flexDirection: 'column-reverse',
                }}
            >
                {chatHistory.map((msg, index) => (
                    <Paper
                        key={index}
                        sx={{
                            padding: 2,
                            marginBottom: 1,
                            maxWidth: '80%',
                            alignContent:'start',
                            alignSelf: msg.isUser ? 'flex-end' : 'flex-start',
                            backgroundColor: msg.isUser ? '#e3f2fd' : '#f1f1f1',
                        }}
                    >
                        <Typography variant="body1">{msg.text}</Typography>
                    </Paper>
                ))}
            </Box>

            {/* Input Area at the Bottom */}
            <Box
                sx={{
                    padding: 2,
                    backgroundColor: '#fff',
                    display: 'flex',
                    alignItems: 'center',
                    borderTop: '1px solid #ddd',
                }}
            >
                <TextField
                    label="Ask a question..."
                    variant="outlined"
                    fullWidth
                    value={message}
                    onKeyDown={handleKeyDown}
                    onChange={handleMessageChange}
                    sx={{
                        marginRight: 2,
                        backgroundColor: '#f5f5f5',
                        borderRadius: 1,
                    }}
                />
                <IconButton
                    variant="contained"
                    color="primary"
                    onClick={handleSendMessage}
                    disabled={!message.trim()} // Disable if message is empty
                >
                    {loading ? (
                        <CircularProgress size={24} sx={{ position: 'absolute' }} />
                    ) : (
                        <Send />
                    )}
                </IconButton>
            </Box>
        </Box>
    );
};

export default ChatInterface;
