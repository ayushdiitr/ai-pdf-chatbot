import React, { useState } from 'react';
import { Box, Button, Typography, CircularProgress } from '@mui/material';
import { useDropzone } from 'react-dropzone';
import UploadFileIcon from '@mui/icons-material/UploadFile';
import axios from 'axios';

const Sidebar = () => {
  const [pdfFile, setPdfFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [responseMessage, setResponseMessage] = useState('');

  // Handle file drop
  const onDrop = (acceptedFiles) => {
    const file = acceptedFiles[0];
    if (file && file.type === 'application/pdf') {
      setPdfFile(file);
    } else {
      alert('Please drop a valid PDF file.');
    }
  };

  // Initialize the dropzone
  const { getRootProps, getInputProps } = useDropzone({
    onDrop,
    accept: '.pdf',  
    maxFiles: 1,      
  });

  // Handle submit
  const handleSubmit = async () => {
    if (pdfFile) {
      setLoading(true);  
      const formData = new FormData();
      formData.append('pdf', pdfFile);

      try {
        const response = await axios.post('http://localhost:8000/api/chat/', formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        });
        setResponseMessage(response.data.message || 'PDF uploaded successfully.');
      } catch (error) {
        setResponseMessage('Failed to upload PDF. Please try again.');
        console.error('Error uploading PDF:', error);
      } finally {
        setLoading(false);  
      }
    } else {
      alert('Please upload a PDF file.');
    }
  };

  return (
    <Box
      sx={{
        width: '300px',
        backgroundColor: '#fff',
        padding: 2,
        boxShadow: 3,
        display: 'flex',
        flexDirection: 'column',
      }}
    >
      {/* Title */}
      <Box sx={{ display: 'flex', flexDirection: 'row', alignItems: 'center', mb: 3 }}>
        <Typography variant="h5" sx={{ fontWeight: 'bold' }}>
          Upload PDF
        </Typography>
        <UploadFileIcon sx={{ marginLeft: 1 }} />
      </Box>

      {/* Drag-and-Drop Area */}
      <Box
        {...getRootProps()}
        sx={{
          border: '2px dashed #1976d2',
          padding: 3,
          height: 200,
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'center',
          alignItems: 'center',
          cursor: 'pointer',
          backgroundColor: '#e3f2fd',
          marginBottom: 2,
        }}
      >
        <input {...getInputProps()} />
        <Typography variant="body2" sx={{ color: '#1976d2', textAlign: 'center' }}>
          Drag and drop a PDF file here, or click to select
        </Typography>
        {pdfFile && (
          <Typography variant="body2" sx={{ marginTop: 1 }}>
            File: {pdfFile.name}
          </Typography>
        )}
      </Box>

      {responseMessage && (
        <Typography variant="body2" sx={{ color: '#1976d2', marginBottom: 2 }}>
          {responseMessage}
        </Typography>
      )}

      <Button
        variant="contained"
        color="primary"
        onClick={handleSubmit}
        fullWidth
        disabled={loading}  
        sx={{ position: 'relative' }}
        startIcon={ loading ? <CircularProgress /> : null }
      >
        {loading ? (
          'Reading PDF...'
        ) : (
          'Submit'
        )}
      </Button>
    </Box>
  );
};

export default Sidebar;
