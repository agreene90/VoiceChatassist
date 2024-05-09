# Voice-Activated Personal Assistant

![Voice-Activated Personal Assistant](chatv2.png)

## Overview
This project implements a sophisticated voice-activated personal assistant that leverages advanced natural language processing (NLP) and speech recognition technologies. It is designed to operate under various environments, ensuring high accuracy and responsiveness for a seamless user interaction experience.

## Key Features
- **Real-Time Speech Recognition**: Utilizes offline capabilities of `speech_recognition` and `pyttsx3` libraries to convert speech to text and vice versa without requiring an internet connection, enhancing privacy and reliability.
- **Advanced NLP Capabilities**: Employs the `spacy` library with its `en_core_web_trf` model, a transformer-based model known for its accuracy in parsing and understanding complex language patterns. This includes robust entity recognition and dependency parsing to comprehend the nuances of human language.
- **Persistent Storage**: Manages interaction logs and adapts responses based on frequency using a SQLite database. Asynchronous operations with `aiosqlite` ensure that data handling is efficient and does not block system responsiveness.
- **Scalable Architecture**: Built to scale easily, the system features comprehensive error handling, robust logging with file rotation, and asynchronous processing capabilities, facilitating easy integration and expansion.

## Installation
To install and run the assistant on your local machine, follow these steps:
```bash
# Clone the repository
git clone https://github.com/agreene90/VoiceChatassist
cd voice-activated-assistant

# Run deployment script
./deploy.sh
```

## Usage
The assistant is designed to process audio data efficiently:
```bash
# Send audio data to the processing endpoint
Send audio data to the `/process/` endpoint via our API to receive a textual response based on the recognized speech and analyzed text.
```
The system handles requests asynchronously, ensuring quick and efficient processing without delays.

## Architecture
Detailed breakdown of the system's modular architecture:
- **Speech Recognition Module**: Handles the conversion of spoken language into text using offline processing, ensuring user data privacy and system reliability.
- **NLP Processing Module**: Utilizes advanced NLP models to analyze text, understand user intent, and generate contextually appropriate responses.
- **Database Interaction Module**: Provides efficient and non-blocking database operations to store interaction logs and manage response adaptation based on user interaction patterns.
- **Utilities Module**: Supports the system infrastructure with logging functionalities that help in monitoring the system's health and troubleshooting issues.

## Deployment
Deployment instructions are simplified for ease of setup:
```bash
# Follow the script to set up the environment
./deploy.sh
```

## License
The project is distributed under the MIT License, which allows modification and distribution of the software under specific conditions. See the `LICENSE` file for more details.
