from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from .chatbot_rag import conversation, run_pdf_qna
from rest_framework.exceptions import ValidationError
import tempfile
import os

class ChatAPIView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    pdf_storage = {}  # Dictionary to store the vector database for each user

    def post(self, request):
        """
        Accepts either a query or a PDF file for processing and returns a response.
        If a PDF is uploaded for the first time, it's processed and stored.
        If a query is provided after PDF upload, the model will use the processed PDF.
        """
        user_id = request.user.id  # Assuming you're using user authentication (e.g., JWT tokens)
        print(user_id, request)
        if 'query' in request.data:
            # If a query is provided, process it
            query = request.data['query']
            history = request.data.get('history', [])

            if user_id not in self.pdf_storage:
                return Response({"error": "No PDF file uploaded. Please upload a PDF first."}, status=status.HTTP_400_BAD_REQUEST)
            
            # Use the vector database from memory (created during the first PDF upload)
            qa_chain = self.pdf_storage[user_id]
            response_answer, source1, source2, source3 = conversation(qa_chain, query, history)

            response_data = {
                "answer": response_answer,
                "source1": source1,
                "source2": source2,
                "source3": source3
            }

            return Response(response_data, status=status.HTTP_200_OK)

        elif 'pdf' in request.FILES:
            # If only PDF is uploaded, save it and initialize the model for the user
            pdf_file = request.FILES['pdf']
            
            with tempfile.NamedTemporaryFile(delete=False) as temp_pdf_file:
                temp_pdf_file.write(pdf_file.read())
                temp_pdf_file_path = temp_pdf_file.name

            # Initialize the model with the uploaded PDF
            qa_chain = run_pdf_qna(temp_pdf_file_path, chunk_size=1500, chunk_overlap=100)
            
            # Store the vector database for the user (in memory or a persistent database)
            self.pdf_storage[user_id] = qa_chain

            return Response({"message": "PDF uploaded and processed successfully. You can now ask questions."}, status=status.HTTP_200_OK)
        
        else:
            return Response({"error": "Please provide either a query or a PDF file."}, status=status.HTTP_400_BAD_REQUEST)
