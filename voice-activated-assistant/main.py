import uvicorn
from fastapi import FastAPI, HTTPException, Depends
import logging
from pydantic import BaseModel
from database_interaction import ChatDatabase
from nlp_processing import analyze_text
from speech_recognition import listen_and_respond

# Initialize the FastAPI app
app = FastAPI()

# Setup logging
logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize the database
database = ChatDatabase('chat_memory.db')

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
    Receives a speech input as text, processes it through NLP, and returns a generated response.
    """
    try:
        user_speech = interaction.speech
        if user_speech:
            response = await analyze_text(user_speech)
            await database.update_response_frequency(response)
            database.log_interaction(user_speech, response)
            return {"response": response}
        else:
            raise HTTPException(status_code=400, detail="No speech detected")
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/response/{response}")
async def get_response_frequency(response: str, database: ChatDatabase = Depends(get_database)):
    """
    Fetches the frequency of how often a particular response has been used.
    """
    try:
        frequency = await database.get_response_frequency(response)
        if frequency is not None:
            return {"response": response, "frequency": frequency}
        else:
            raise HTTPException(status_code=404, detail="Response not found")
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/listen/")
async def listen_and_process(database: ChatDatabase = Depends(get_database)):
    """
    Listens to live speech using the system's microphone, converts it to text, analyzes the text, and returns a response.
    """
    try:
        user_speech = listen_and_respond()
        if user_speech:
            response = await analyze_text(user_speech)
            await database.update_response_frequency(response)
            database.log_interaction(user_speech, response)
            return {"response": response}
        else:
            raise HTTPException(status_code=400, detail="No speech detected")
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    # Start the Uvicorn server to run the application
    uvicorn.run(app, host="0.0.0.0", port=5000)