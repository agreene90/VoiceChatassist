import logging
import re
from dateutil.parser import parse
import spacy
import nltk
from nltk.tokenize import word_tokenize
import requests
from bs4 import BeautifulSoup

# Initialize the logger
logging.basicConfig(level=logging.INFO)

# Load spaCy model for English
nlp = spacy.load('en_core_web_trf')

# Download NLTK resources
nltk.download('punkt')

def extract_entities(text):
    # Extract named entities using spaCy's NER
    doc = nlp(text)
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    return entities

def parse_dates(text):
    # Parse dates using spaCy's NER and fallback to dateutil.parser
    doc = nlp(text)
    dates = [ent.text for ent in doc.ents if ent.label_ == 'DATE']
    parsed_dates = []
    for date in dates:
        try:
            parsed_date = parse(date, fuzzy=True)
            parsed_dates.append(parsed_date.strftime('%Y-%m-%d'))
        except ValueError:
            logging.warning(f'Could not parse date: {date}')
    return parsed_dates

def analyze_text(text):
    # Extract named entities using spaCy's NER
    entities = extract_entities(text)
    logging.info(f'Named entities: {entities}')
    
    # Parse dates using spaCy's NER and dateutil.parser
    parsed_dates = parse_dates(text)
    logging.info(f'Parsed dates: {parsed_dates}')
    
    # Tokenize text using NLTK
    tokens = word_tokenize(text)
    
    # Check for greetings using regular expressions for robust pattern matching
    greeting_patterns = [r'\b(?:hello|hi|hey)\b', r'^(?:[Hh]ello|[Hh]i|[Hh]ey)[,.!?\s]+']
    for pattern in greeting_patterns:
        if re.search(pattern, text):
            logging.info('Found a greeting')
            return 'Found a greeting'
    
    # Process the text with spaCy for dependency parsing and part-of-speech tagging
    doc = nlp(text)
    
    # Check for weather inquiries using spaCy dependency parsing
    for token in doc:
        if token.lower_ == 'weather':
            weather_inquiry_patterns = [r'\b(?:like|forecast|temperature)\b', r'(?:like|forecast|temperature)[,.!?\s]+']
            for child in token.children:
                for pattern in weather_inquiry_patterns:
                    if re.search(pattern, child.text, re.IGNORECASE):
                        logging.info('Found a weather inquiry')
                        return 'Found a weather inquiry'
    
    return 'No matches found.'

def scrape_web_page(url):
    try:
        # Send a GET request to the URL
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes
        
        # Parse the HTML content of the web page
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract relevant information from the web page
        # Example: Extract text from all paragraphs
        paragraphs = soup.find_all('p')
        text_content = '\n'.join(paragraph.text for paragraph in paragraphs)
        
        # Analyze the extracted text
        result = analyze_text(text_content)
        return result
    
    except Exception as e:
        logging.error(f"An error occurred while scraping the web page: {str(e)}")
        return 'Error: Could not scrape the web page.'

if __name__ == "__main__":
    while True:
        input_text = input("Enter some text or a URL to scrape: ")
        if input_text.startswith("http://") or input_text.startswith("https://"):
            result = scrape_web_page(input_text)
        else:
            result = analyze_text(input_text)
        print(result)