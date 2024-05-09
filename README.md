
# Voice-Activated Personal Assistant

![Voice-Activated Personal Assistant](chatv2.png)

## Overview
This project implements a sophisticated voice-activated personal assistant utilizing advanced NLP and speech recognition technologies to understand and process audio inputs efficiently. Designed to perform under various environments, our assistant ensures high accuracy and responsiveness, providing users with a seamless interaction experience.

## Key Features
- **Real-Time Speech Recognition**: Leverages the robust Vosk model to convert speech into text accurately.
- **Advanced NLP Capabilities**: Uses state-of-the-art models like BERT for sentiment analysis and GPT for generating context-aware dialogues.
- **Persistent Storage**: Interaction logs are maintained in a SQLite database for future reference and analysis.
- **Scalable Architecture**: Designed to be scalable with microservices-ready capabilities for easy integration and expansion.

## Installation
Clone the repository to your local machine and navigate to the project directory:
```bash
git clone https://github.com/agreene90/VoiceChatassist
cd voice-activated-assistant
```
Run `deploy.sh` to set up the environment and start the application:
```bash
./deploy.sh
```

## Usage
Send audio data to the `/listen` endpoint via our API to receive a textual response based on the sentiment analysis of the spoken input. The system handles requests asynchronously, ensuring efficient processing.

## Architecture
The assistant's architecture includes several modules:
- **Speech Recognition**: Converts spoken language into text.
- **NLP Processing**: Analyzes sentiment and generates responses.
- **Database Interaction**: Manages interaction logs for in-depth analysis.
- **Utilities**: Provides logging and other backend utilities.

## Deployment
Follow the instructions in `deploy.sh` to deploy the application on any server with minimal setup.

## Contributing
Contributions to improve the assistant are welcome. Please fork the repository, make your changes, and submit a pull request to the main branch.

For more information, contact [contact-information].

## License
Distributed under the MIT License. See `LICENSE` for more information.
