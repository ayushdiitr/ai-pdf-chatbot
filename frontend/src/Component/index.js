import { Box, Stack } from '@mui/material'
import React from 'react'
import Sidebar from './Sidebar'
import ChatInterface from './Chat'

function Main() {
    return (
        <Box sx={{ height: '100vh', }}>
            <Box flex={1} sx={{ display: 'flex', height: "100vh", zIndex:10 }}>
                <Sidebar />
                <Stack direction="column" flex={1} sx={{ height: "100vh", width: "100%", overflow: 'hidden' }} >
                    <ChatInterface />                    
                </Stack>
            </Box>
        </Box>)
}

export default Main