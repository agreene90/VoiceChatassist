import speech_recognition as sr
import pyttsx3
import logging

# Initialize the speech engine
engine = pyttsx3.init()
recognizer = sr.Recognizer()
microphone = sr.Microphone()

def listen_and_respond():
    try:
        with microphone as source:
            recognizer.adjust_for_ambient_noise(source)
            logging.info("Listening for speech...")
            audio = recognizer.listen(source)
            text = recognizer.recognize_google(audio)
            engine.say(f"You said: {text}")
            engine.runAndWait()
            return text
    except sr.UnknownValueError:
        engine.say("I didn't catch that. Could you please repeat?")
        engine.runAndWait()
        return listen_and_respond()  # Retry mechanism
    except sr.RequestError as e:
        logging.error(f"Speech recognition service error: {e}")
        engine.say("I'm having trouble with the speech service right now.")
        engine.runAndWait()
        return None

if __name__ == "__main__":
    while True:
        listen_and_respond()