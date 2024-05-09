
from transformers import pipeline
import logging
import os

sentiment_model_path = os.getenv('SENTIMENT_MODEL_PATH', 'models/bert-sentiment-model')
dialogue_model_path = os.getenv('DIALOGUE_MODEL_PATH', 'models/gpt2-dialogue-model')

try:
    sentiment_analysis = pipeline('sentiment-analysis', model=sentiment_model_path)
    dialogue_manager = pipeline('text-generation', model=dialogue_model_path)
except Exception as e:
    logging.error(f"Failed to load models: {str(e)}")
    raise ImportError("Could not load NLP models.")

def analyze_sentiment(text):
    try:
        result = sentiment_analysis(text)[0]
        return result['label']
    except Exception as e:
        logging.error(f"Error analyzing sentiment: {str(e)}")
        raise ValueError("Sentiment analysis failed.")

def generate_response(text, sentiment):
    try:
        adjusted_input = f"{text} {'Positive' if sentiment == 'POSITIVE' else 'Negative'} mood detected."
        response = dialogue_manager(adjusted_input)[0]['generated_text']
        return response
    except Exception as e:
        logging.error(f"Error generating response: {str(e)}")
        raise ValueError("Response generation failed.")
