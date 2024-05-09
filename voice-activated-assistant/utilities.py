import logging
from logging.handlers import RotatingFileHandler

# Setup logging with rotation to manage log file size
log_file = 'system_logs.log'
logging.basicConfig(handlers=[RotatingFileHandler(log_file, maxBytes=1000000, backupCount=5)],
                    level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def log_interaction(text, response):
    # Log the interaction details
    logging.info(f'Processed interaction: Text: "{text}" -> Response: "{response}"')

def log_error(message):
    # Log any errors that occur
    logging.error(message)

def log_info(message):
    # Log general information
    logging.info(message)

if __name__ == "__main__":
    # Example usage of logging functions
    log_interaction("Hello", "Hi there!")
    log_error("This is an error message.")
    log_info("This is a general information message.")