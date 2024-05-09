#!/bin/bash

# Define the script's exit on error
set -e

echo "Starting deployment of the voice-activated personal assistant."

# Create and activate a Python virtual environment
echo "Creating and activating a virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Set environment variables
echo "Setting up environment variables..."
export DATABASE_PATH="chat_memory.db"
export MODEL_PATH="models/"

# Upgrade pip to its latest version
echo "Upgrading pip..."
pip install --upgrade pip

# Install required Python packages locally
echo "Installing required Python packages..."
pip install fastapi uvicorn sqlalchemy aiosqlite spacy pyttsx3 speech_recognition streamlit streamlit_webrtc

# Download and setup SpaCy models
echo "Downloading and setting up SpaCy models..."
python -m spacy download en_core_web_trf

# Install NLTK data
echo "Installing NLTK data..."
python -m nltk.downloader punkt

# Ensure the database is initialized properly with error handling
echo "Initializing the database..."
python -c 'import asyncio; from database_interaction import ChatDatabase; db = ChatDatabase("$DATABASE_PATH"); asyncio.run(db.init_db())' || echo "Failed to initialize the database. Check the logs for details."

# Start the application
echo "Starting the application..."
uvicorn main:app --host 0.0.0.0 --port 5000 || echo "Failed to start the application. Check the logs for details."

echo "Deployment complete."

# Deactivate the virtual environment
deactivate

# Script exit point
echo "Script completed successfully."