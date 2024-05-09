# Voice-Activated Personal Assistant

![Voice-Activated Personal Assistant](chatv2.png)

## Overview
This project implements a sophisticated voice-activated personal assistant utilizing advanced NLP and speech recognition technologies to understand and process audio inputs efficiently. Designed to perform under various environments, our assistant ensures high accuracy and responsiveness, providing users with a seamless interaction experience.

## Key Features
- **Real-Time Speech Recognition**: Uses offline capabilities of `speech_recognition` and `pyttsx3` for accurate conversion of speech to text and vice versa, entirely offline.
- **Advanced NLP Capabilities**: Employs `spacy` with the `en_core_web_trf` model for robust text processing, including entity recognition and dependency parsing.
- **Persistent Storage**: Interaction logs and response frequencies are maintained in a SQLite database using asynchronous operations with `aiosqlite`, ensuring high-performance data handling.
- **Scalable Architecture**: Designed to be scalable with comprehensive error handling, logging, and asynchronous processing capabilities for easy integration and expansion.

## Installation
Clone the repository to your local machine and navigate to the project directory:
```bash
git clone [repository-url]
cd voice-activated-assistant
```
Run `deploy.sh` to set up the environment and start the application:
```bash
./deploy.sh
```

## Usage
Send audio data to the `/process/` endpoint via our API to receive a textual response based on the recognized speech and analyzed text. The system handles requests asynchronously, ensuring efficient processing.

## Architecture
The assistant's architecture includes several modules:
- **Speech Recognition**: Converts spoken language into text and vice versa, entirely offline.
- **NLP Processing**: Analyzes text using advanced models to understand content and context.
- **Database Interaction**: Manages interaction logs for in-depth analysis with efficient, non-blocking database operations.
- **Utilities**: Provides robust logging and other backend utilities.

## Deployment
Follow the instructions in `deploy.sh` to deploy the application on any server with minimal setup.

## License
Distributed under the MIT License. See `LICENSE` for more information.