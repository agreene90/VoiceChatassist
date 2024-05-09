
import logging
from vosk import Model, KaldiRecognizer
import json
import os

model_path = os.getenv('VOSK_MODEL_PATH', 'models/vosk-model-small-en-us-0.15')
model = Model(model_path)
recognizer = KaldiRecognizer(model, 16000)

async def recognize_audio(audio_data):
    try:
        if recognizer.AcceptWaveform(audio_data):
            result = json.loads(recognizer.Result())
            text = result['text']
            logging.info(f"Recognized speech: {text}")
            return text
        else:
            return "I didn't catch that. Could you please repeat?"
    except Exception as e:
        logging.error(f"Error in speech recognition: {str(e)}")
        raise Exception("Speech recognition failed due to an internal error.")
