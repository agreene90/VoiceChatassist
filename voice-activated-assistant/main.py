import streamlit as st
from streamlit_webrtc import webrtc_streamer, RTCConfiguration, VideoTransformerBase
import pyttsx3
import asyncio
import logging

# Custom modules
from utilities import CustomLogger
from database_interaction import ChatDatabase
from ML import MLModel  # Importing the MLModel from ML.py
from nlp_processing import listen_and_respond  # Import listen_and_respond from your nlp_processing script

# Setup custom logging
logger = CustomLogger('app.log', max_bytes=1000000, backup_count=5)

# Initialize the text-to-speech engine
tts_engine = pyttsx3.init()

# Initialize the ML Model
ml_model = MLModel(logger)

# Initialize the database connection
db = ChatDatabase('chat_memory.db')
asyncio.run(db.init_db())  # Ensure the database is initialized

# WebRTC configuration
RTC_CONFIGURATION = RTCConfiguration(
    {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
)

class AudioProcessor(VideoTransformerBase):
    def recv(self, frame):
        data = frame.to_ndarray(format="mono")
        text = listen_and_respond(data)  # Use the listen_and_respond function to process audio
        response = asyncio.run(ml_model.summarize_text(text))
        sentiment_score = asyncio.run(ml_model.analyze_sentiment(text))
        asyncio.run(db.update_response_frequency(response))
        logger.log_interaction(text, response)
        tts_engine.say(response)
        tts_engine.runAndWait()
        return frame

def main():
    st.title('Voice-Activated Personal Assistant')
    st.text('Speak into your microphone and the assistant will respond.')
    
    # WebRTC streamer for real-time audio processing
    webrtc_streamer(key="audio_processor",
                    video_transformer_factory=AudioProcessor,
                    rtc_configuration=RTC_CONFIGURATION,
                    media_stream_constraints={"video": False, "audio": True})

if __name__ == "__main__":
    main()