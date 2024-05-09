import uvicorn
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from database_interaction import ChatDatabase
from nlp_processing import analyze_text
from speech_recognition import listen_and_respond
from utilities import CustomLogger  # Importing CustomLogger from utilities.py
import pyttsx3  # Importing the pyttsx3 library for text-to-speech

# Initialize the FastAPI app
app = FastAPI()

# Setup custom logging
logger = CustomLogger('app.log', max_bytes=1000000, backup_count=5)

# Initialize the database
database = ChatDatabase('chat_memory.db')

# Initialize the text-to-speech engine
tts_engine = pyttsx3.init()

class Interaction(BaseModel):
    speech: str

def get_database():
    try:
        yield database
    finally:
        database.close()

@app.post("/process/")
async def process_audio(interaction: Interaction, database: ChatDatabase = Depends(get_database)):
    """
    Receives a speech input as text, processes it through NLP, and returns a generated response in spoken form.
    """
    try:
        user_speech = interaction.speech
        if user_speech:
            response = await analyze_text(user_speech)
            await database.update_response_frequency(response)
            logger.log_interaction(user_speech, response)  # Using custom logger
            tts_engine.say(response)
            tts_engine.runAndWait()
            return {"response": response}
        else:
            raise HTTPException(status_code=400, detail="No speech detected")
    except Exception as e:
        logger.log_error(f"An error occurred: {str(e)}")  # Using custom logger
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/listen/")
async def listen_and_process(database: ChatDatabase = Depends(get_database)):
    """
    Listens to live speech using the system's microphone, converts it to text, analyzes the text, and returns a spoken response.
    """
    try:
        user_speech = listen_and_respond()
        if user_speech:
            response = await analyze_text(user_speech)
            await database.update_response_frequency(response)
            logger.log_interaction(user_speech, response)  # Using custom logger
            tts_engine.say(response)
            tts_engine.runAndWait()
            return {"response": response}
        else:
            raise HTTPException(status_code=400, detail="No speech detected")
    except Exception as e:
        logger.log_error(f"An error occurred: {str(e)}")  # Using custom logger
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    # Start the Uvicorn server to run the application
    uvicorn.run(app, host="0.0.0.0", port=5000)