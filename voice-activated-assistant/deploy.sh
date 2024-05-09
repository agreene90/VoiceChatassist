#!/bin/bash

echo "Starting deployment of the voice-activated personal assistant."

# Set environment variables
echo "Setting up environment variables..."
export DATABASE_PATH="chat_memory.db"
export MODEL_PATH="models/"

# Install required Python packages locally
echo "Installing required Python packages..."
pip install fastapi uvicorn sqlalchemy aiosqlite spacy pyttsx3 speech_recognition

# Download and setup SpaCy models
echo "Downloading and setting up SpaCy models..."
python -m spacy download en_core_web_trf

# Initialize the database
echo "Initializing database..."
python -c 'import asyncio; from database_interaction import init_db; asyncio.run(init_db())'

# Start the application
echo "Starting the application..."
uvicorn main:app --host 0.0.0.0 --port 5000