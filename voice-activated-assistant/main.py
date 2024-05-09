import uvicorn
from fastapi import FastAPI, HTTPException
import asyncio
import logging
from speech_recognition import listen_and_respond
from nlp_processing import analyze_text
from database_interaction import update_response_frequency
from utilities import log_interaction, log_error

# Initialize the FastAPI app
app = FastAPI()

# Setup logging
logging.basicConfig(level=logging.INFO)

@app.post("/process/")
async def process_audio():
    try:
        # Listen to the user and convert speech to text
        user_speech = await asyncio.to_thread(listen_and_respond)
        if user_speech:
            # Analyze the text for patterns and generate a response
            response = analyze_text(user_speech)
            # Update the frequency of the response
            await update_response_frequency(response)
            # Log the interaction
            log_interaction(user_speech, response)
            return {"response": response}
        else:
            raise HTTPException(status_code=400, detail="No speech detected")
    except Exception as e:
        log_error(f"An error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    # Start the Uvicorn server to run the application
    uvicorn.run(app, host="0.0.0.0", port=5000)