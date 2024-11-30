import os
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain.chains import ConversationalRetrievalChain
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.llms import HuggingFaceEndpoint
from langchain.memory import ConversationBufferMemory
from pathlib import Path
import chromadb
from unidecode import unidecode
import re
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("API_KEY")

# List of available LLM models (only using Mistral-7B for now)
list_llm = ["mistralai/Mistral-7B-Instruct-v0.2"]  # Only using Mistral-7B

# Hugging Face login using the provided token
def hf_login(token: str):
    api_key

# Load PDF document and create document splits
def load_doc(file_path, chunk_size, chunk_overlap):
    loader = PyPDFLoader(file_path)
    pages = loader.load()
    
    # Adjusting chunk size and overlap for larger files
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len  # More efficient length calculation for large docs
    )
    
    doc_splits = text_splitter.split_documents(pages)
    
    # Remove redundant or irrelevant sources (e.g., repeated instructions)
    doc_splits = remove_redundant_sources(doc_splits)
    
    return doc_splits

# Function to remove redundant sources
def remove_redundant_sources(doc_splits):
    seen_sources = set()
    filtered_splits = []
    
    for split in doc_splits:
        clean_text = split.page_content.strip()
        if clean_text and clean_text not in seen_sources:
            filtered_splits.append(split)
            seen_sources.add(clean_text)
    
    return filtered_splits

# Create vector database
def create_db(splits, collection_name):
    embedding = HuggingFaceEmbeddings()
    new_client = chromadb.EphemeralClient()
    
    # Creating the vector database in chunks to avoid memory overload
    vectordb = Chroma.from_documents(
        documents=splits,
        embedding=embedding,
        client=new_client,
        collection_name=collection_name,
    )
    return vectordb

# Generate collection name for vector database based on the file path
def create_collection_name(filepath):
    collection_name = Path(filepath).stem
    collection_name = collection_name.replace(" ", "-")  # Remove space
    collection_name = unidecode(collection_name)  # Convert to ASCII
    collection_name = re.sub('[^A-Za-z0-9]+', '-', collection_name)  # Remove special characters
    collection_name = collection_name[:50]  # Limit length
    if len(collection_name) < 3:
        collection_name += 'xyz'  # Ensure minimum length
    if not collection_name[0].isalnum():
        collection_name = 'A' + collection_name[1:]
    if not collection_name[-1].isalnum():
        collection_name = collection_name[:-1] + 'Z'
    return collection_name

# Initialize LLM chain
def initialize_llmchain(llm_model, temperature, max_tokens, top_k, vector_db):
    llm = HuggingFaceEndpoint(
        repo_id=llm_model,
        temperature=temperature,
        max_new_tokens=max_tokens,
        top_k=top_k,
        huggingfacehub_api_token=api_key,
        
    )
    memory = ConversationBufferMemory(memory_key="chat_history", output_key='answer', return_messages=True)
    retriever = vector_db.as_retriever()
    qa_chain = ConversationalRetrievalChain.from_llm(
        llm,
        retriever=retriever,
        chain_type="stuff",
        memory=memory,
        return_source_documents=True,
    )
    return qa_chain

# Initialize database (load and process PDF, create vector database)
def initialize_database(file_path, chunk_size, chunk_overlap):
    collection_name = create_collection_name(file_path)
    doc_splits = load_doc(file_path, chunk_size, chunk_overlap)
    vector_db = create_db(doc_splits, collection_name)
    return vector_db, collection_name

# Generate response from QA chain
def conversation(qa_chain, message, history):
    formatted_chat_history = format_chat_history(message, history)
    response = qa_chain({"question": message, "chat_history": formatted_chat_history})
    response_answer = response["answer"]
    
    if not response_answer.strip():  # If no answer found, fallback response
        response_answer = "Sorry, I didn’t understand your question. Do you want to connect with a live agent?"
    
    response_sources = response["source_documents"]
    response_source1 = response_sources[0].page_content.strip() if len(response_sources) > 0 else ""
    response_source2 = response_sources[1].page_content.strip() if len(response_sources) > 1 else ""
    response_source3 = response_sources[2].page_content.strip() if len(response_sources) > 2 else ""
    
    return response_answer, response_source1, response_source2, response_source3

# Format chat history for the conversation model
def format_chat_history(message, chat_history):
    formatted_chat_history = []
    for user_message, bot_message in chat_history:
        formatted_chat_history.append(f"User: {user_message}")
        formatted_chat_history.append(f"Assistant: {bot_message}")
    return formatted_chat_history

# Main function to run the Q&A process
def run_pdf_qna(file_path, chunk_size=1500, chunk_overlap=100, temperature=0.7, max_tokens=1024, top_k=3, hf_token=api_key):
    if hf_token:
        hf_login(hf_token)  # Authenticate with Hugging Face using the provided token
    
    vector_db, collection_name = initialize_database(file_path, chunk_size, chunk_overlap)
    llm_model = list_llm[0]  # Only using the first model (Mistral-7B)
    qa_chain = initialize_llmchain(llm_model, temperature, max_tokens, top_k, vector_db)
    
    print(f"PDF loaded and vector database '{collection_name}' created.")
    return qa_chain

# Example usage
if __name__ == "__main__":
    hf_token = input("Please enter your Hugging Face token (or leave empty if not using): ")
    file_path = input("Please enter the path to your PDF document: ")  # Ask user for PDF path
    qa_chain = run_pdf_qna(file_path, hf_token=hf_token)

    while True:
        question = input("Ask a question or type 'exit' to quit: ")
        if question.lower() == 'exit':
            break
        
        history = []  # Initialize empty history
        answer, source1, source2, source3 = conversation(qa_chain, question, history)
        
        print(f"Answer: {answer}")
        if source1:
            print(f"Source 1: {source1}")
        if source2:
            print(f"Source 2: {source2}")
        if source3:
            print(f"Source 3: {source3}")
