import spacy
from spacy.matcher import Matcher
import logging

# Initialize the logger
logging.basicConfig(level=logging.INFO)

# Load Spacy model for English
nlp = spacy.load('en_core_web_trf')
matcher = Matcher(nlp.vocab)

def setup_matcher():
    # Define patterns to match in the text
    greeting_patterns = [[{'LOWER': 'hello'}], [{'LOWER': 'goodbye'}]]
    weather_patterns = [[{'LOWER': 'weather'}, {'LOWER': 'like', 'OP': '?'}]]
    
    # Add patterns to the matcher
    for pattern in greeting_patterns:
        matcher.add('Greeting', [pattern])
    for pattern in weather_patterns:
        matcher.add('Weather Inquiry', [pattern])

def analyze_text(text):
    # Process the text with the NLP model
    doc = nlp(text)
    matches = matcher(doc)
    
    # Check for matches and log them
    for match_id, start, end in matches:
        span = doc[start:end]
        logging.info(f'Found a match: {span.text}')
        return f'Found a match: {span.text}'
    return 'No matches found.'

if __name__ == "__main__":
    setup_matcher()
    while True:
        input_text = input("Enter some text: ")
        result = analyze_text(input_text)
        print(result)