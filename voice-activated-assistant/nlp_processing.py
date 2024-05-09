import spacy
import logging
from dateutil.parser import parse

# Initialize the logger
logging.basicConfig(level=logging.INFO)

# Load Spacy model for English with NER
nlp = spacy.load('en_core_web_trf')

def analyze_text(text):
    # Process the text with the NLP model
    doc = nlp(text)
    
    # Extract named entities
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    logging.info(f'Named entities: {entities}')
    
    # Check for dates and parse them
    dates = [token.text for token in doc if token.ent_type_ == 'DATE']
    parsed_dates = []
    for date in dates:
        try:
            parsed_date = parse(date, fuzzy=True)
            parsed_dates.append(parsed_date.strftime('%Y-%m-%d'))
        except ValueError:
            logging.warning(f'Could not parse date: {date}')
    
    logging.info(f'Parsed dates: {parsed_dates}')
    
    # Check for greetings
    for token in doc:
        if any(token.text.lower() in greeting for greeting in ['hello', 'hi', 'hey']):
            logging.info(f'Found a greeting: {token.text}')
            return f'Found a greeting: {token.text}'
    
    # Check for weather inquiries
    for token in doc:
        if token.lower_ == 'weather' and any(next_token.lower_ in ['like', 'forecast', 'temperature'] for next_token in doc[token.i + 1:token.i + 4]):
            logging.info('Found a weather inquiry')
            return 'Found a weather inquiry'
    
    return 'No matches found.'

if __name__ == "__main__":
    while True:
        input_text = input("Enter some text: ")
        result = analyze_text(input_text)
        print(result)