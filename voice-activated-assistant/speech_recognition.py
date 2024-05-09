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

def listen_and_respond():
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        logging.info("Listening for speech...")
        try:
            audio = recognizer.listen(source)
            text = recognizer.recognize_google(audio)
            logging.info(f"Recognized speech: {text}")
            engine.say(f"You said: {text}")
            engine.runAndWait()
            return text
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