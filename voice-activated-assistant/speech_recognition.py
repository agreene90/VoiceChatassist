import re
import speech_recognition as sr
import pyttsx3
import logging

# Initialize the logger
logging.basicConfig(level=logging.INFO)

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Initialize the speech recognition
recognizer = sr.Recognizer()
microphone = sr.Microphone()

def dynamic_response(text):
    # Define patterns for dynamic responses
    pattern_greeting = re.compile(r'hello|hi|hey', re.IGNORECASE)
    pattern_question = re.compile(r'how are you', re.IGNORECASE)
    
    # Match patterns
    if pattern_greeting.search(text):
        return "Hello! How can I assist you today?"
    elif pattern_question.search(text):
        return "I'm just a computer program, but thank you for asking!"
    else:
        return None

def listen_and_respond():
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        logging.info("Listening for speech...")
        try:
            audio = recognizer.listen(source)
            text = recognizer.recognize_google(audio)
            logging.info(f"Recognized speech: {text}")
            clean_text = re.sub(r'[^a-zA-Z0-9\s]', '', text)  # Remove special characters
            response = dynamic_response(clean_text)
            if response:
                engine.say(response)
            else:
                engine.say(f"You said: {clean_text}")
            engine.runAndWait()
            return clean_text
        except sr.UnknownValueError:
            logging.error("Speech recognition could not understand audio")
            engine.say("I didn't catch that. Could you please repeat?")
            engine.runAndWait()
        except sr.RequestError as e:
            logging.error(f"Speech recognition service error: {e}")
            engine.say("I'm having trouble with the speech service right now.")
            engine.runAndWait()

if __name__ == "__main__":
    while True:
        listen_and_respond()