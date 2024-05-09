
#!/bin/bash
echo "Starting deployment of the voice-activated personal assistant."

# Environment setup
echo "Setting up environment variables..."
export DATABASE_PATH=chat_memory.db
export VOSK_MODEL_PATH=models/vosk-model-small-en-us-0.15
export SENTIMENT_MODEL_PATH=models/bert-sentiment-model
export DIALOGUE_MODEL_PATH=models/gpt2-dialogue-model

# Install dependencies
echo "Installing required Python packages..."
pip install fastapi uvicorn sqlalchemy aiosqlite vosk transformers

# Initialize the database
echo "Initializing database..."
python -c 'import database_interaction; asyncio.run(database_interaction.init_db())'

# Run the application
echo "Starting the application..."
uvicorn main:app --host 0.0.0.0 --port 5000
