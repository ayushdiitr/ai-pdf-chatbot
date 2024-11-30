
# AI Chatbot for PDF Question Answering

This project is a web-based chatbot application that can answer questions based on the content of a provided PDF document. The system is composed of two main parts: the frontend built with ReactJS and Material-UI (MUI), and the backend developed in Django with a machine learning (ML) model to process and retrieve answers from the PDF content.


## Features

- **Upload PDF**: Users can upload a PDF document for the chatbot to process.
- **Ask Questions**: Once the PDF is uploaded, users can ask questions related to the content of the document.
- The backend uses machine learning models to extract relevant answers from the PDF.




## Project Structure

### Frontend:
The frontend is built using ReactJS and Material-UI to create a responsive and dynamic UI.

### Backend:
The backend is implemented using Django and handles the following:

- **PDF Processing**: Extracts text content from the uploaded PDF.
- **Machine Learning Model**: An ML model is used to answer questions by matching user queries with relevant parts of the document.
- **API Endpoints**: REST API endpoints are provided to handle PDF uploads, user queries, and answer responses.

### ML Model:
The ML model is used to process the text extracted from the PDF and generate relevant answers based on the user's questions.

## Setup

Prerequisites:
   - Python 3.8+
   - Node.js and npm (for frontend)
   - Django
   - ReactJS
   - Required Python packages for the backend (can be installed via `requirements.txt` )
   - Required npm packages for the frontend (can be installed via `npm install` )



## Installation

  ### Backend (Django)

- Clone the repo & intall packages

  ```bash
    git clone https://github.com/ayushdiitr/ai-pdf-chatbot
    cd app
    pip install -r requirements.txt
  ```
- Apply database migrations
  
  ```bash
  python manage.py migrate
  ```
- Create .env
  
  ```bash
  API_KEY='your_hf_secret_key_here'
  ```
- Start Django server
  
  ```bash
  python manage.py runserver
  ```

  ### Frontend (ReactJS)

- Navigate to Frontend directory & install packages

  ```bash
    cd frontend &&
    npm install
  ```

- Start React development server
  
  ```bash
  npm start

  ```


    