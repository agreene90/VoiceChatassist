
import logging
from logging.handlers import RotatingFileHandler

# Setup logger
log_file = 'interaction_logs.log'
logging.basicConfig(handlers=[RotatingFileHandler(log_file, maxBytes=1000000, backupCount=5)],
                    level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def log_interaction(text, response):
    logging.info(f"Processed interaction: Text: {text} -> Response: {response}")
