
import uvicorn
from fastapi import FastAPI, HTTPException, Request, Depends
from pydantic import BaseModel
import asyncio
import logging
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware

import speech_recognition as sr_module
import nlp_processing
import database_interaction
import utilities
import os

# Configure logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

app = FastAPI()

# Middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Authentication configuration
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class AudioRequest(BaseModel):
    audio_data: bytes

@app.post("/listen")
async def listen(audio_request: AudioRequest, token: str = Depends(oauth2_scheme)):
    try:
        text = await sr_module.recognize_audio(audio_request.audio_data)
        sentiment = nlp_processing.analyze_sentiment(text)
        response = nlp_processing.generate_response(text, sentiment)
        await database_interaction.store_interaction(text, response)
        utilities.log_interaction(text, response)
        return {"response": response}
    except Exception as e:
        logging.error(f"Error processing request: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    database_path = os.getenv('DATABASE_PATH', 'chat_memory.db')
    asyncio.run(database_interaction.init_db(database_path))
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', 5000))
    uvicorn.run(app, host=host, port=port)
