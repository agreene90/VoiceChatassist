import uvicorn
from fastapi import FastAPI, HTTPException, Query, Path, Depends
import asyncio
import logging
from speech_recognition import listen_and_respond
from nlp_processing import analyze_text
from database_interaction import ChatDatabase
from pydantic import BaseModel

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
    try:
        user_speech = interaction.speech
        # Listen to the user and convert speech to text
        if user_speech:
            # Analyze the text for patterns and generate a response
            response = await analyze_text(user_speech)
            # Update the frequency of the response
            await database.update_response_frequency(response)
            # Log the interaction
            database.log_interaction(user_speech, response)
            return {"response": response}
        else:
            raise HTTPException(status_code=400, detail="No speech detected")
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/response/{response}")
async def get_response_frequency(response: str = Path(..., title="Response", description="The response to get frequency for"),
                                 database: ChatDatabase = Depends(get_database)):
    try:
        frequency = await database.get_response_frequency(response)
        if frequency is not None:
            return {"response": response, "frequency": frequency}
        else:
            raise HTTPException(status_code=404, detail="Response not found")
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    # Start the Uvicorn server to run the application
    uvicorn.run(app, host="0.0.0.0", port=5000)