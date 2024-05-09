import spacy
from spacy.lang.en import English
import logging

# Load the spaCy model
nlp = spacy.load('en_core_web_sm')

def analyze_text(text):
    try:
        doc = nlp(text)
        # Extract entities and intents
        entities = [(ent.text, ent.label_) for ent in doc.ents]
        intents = [token.lemma_ for token in doc if token.pos_ == 'VERB']
        logging.info(f"Processed text: Entities: {entities}, Intents: {intents}")
        return entities, intents
    except Exception as e:
        logging.error(f"Failed to analyze text: {e}")
        return [], []

if __name__ == "__main__":
    text = "Schedule a meeting at 10 AM"
    analyze_text(text)