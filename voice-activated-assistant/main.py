import uvicorn
from fastapi import FastAPI, WebSocket, HTTPException, Depends, WebSocketDisconnect
from pydantic import BaseModel
from typing import List
import pyttsx3

# Custom modules and ML model
from utilities import CustomLogger
from database_interaction import ChatDatabase
from speech_recognition import listen_and_respond
from ML import MLModel  # Importing the MLModel from ML.py

app = FastAPI()

# Setup custom logging
logger = CustomLogger('app.log', max_bytes=1000000, backup_count=5)

# Initialize the text-to-speech engine
tts_engine = pyttsx3.init()

# Initialize the ML Model
ml_model = MLModel(logger)

# Database Connection Dependency
def get_database():
    db = ChatDatabase('chat_memory.db')
    try:
        yield db
    finally:
        db.close()

class Interaction(BaseModel):
    speech: str

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

@app.websocket("/ws/chat")
async def websocket_endpoint(websocket: WebSocket, db: ChatDatabase = Depends(get_database)):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            sentiment_score = ml_model.analyze_sentiment(data)
            response = await ml_model.summarize_text(data)
            await db.update_response_frequency(response)
            logger.log_interaction(data, response)
            tts_engine.say(response)
            tts_engine.runAndWait()
            await manager.send_personal_message(f"Response: {response}, Sentiment: {sentiment_score}", websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        logger.log_error("WebSocket disconnected")

@app.post("/process/")
async def process_audio(interaction: Interaction, db: ChatDatabase = Depends(get_database)):
    try:
        user_speech = interaction.speech
        if user_speech:
            sentiment_score = ml_model.analyze_sentiment(user_speech)
            response = await ml_model.summarize_text(user_speech)
            await db.update_response_frequency(response)
            logger.log_interaction(user_speech, response)
            tts_engine.say(response)
            tts_engine.runAndWait()
            return {"response": response, "sentiment": sentiment_score}
        else:
            raise HTTPException(status_code=400, detail="No speech detected")
    except Exception as e:
        logger.log_error(f"An error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
