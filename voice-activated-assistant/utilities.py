import logging
from logging.handlers import RotatingFileHandler

class CustomLogger:
    def __init__(self, log_file, max_bytes=1000000, backup_count=5):
        self.log_file = log_file
        self.max_bytes = max_bytes
        self.backup_count = backup_count
        self.setup_logging()

    def setup_logging(self):
        # Configure logging with rotation to manage log file size
        logging.basicConfig(handlers=[RotatingFileHandler(self.log_file, maxBytes=self.max_bytes, backupCount=self.backup_count)],
                            level=logging.INFO,
                            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    def log_interaction(self, text, response):
        # Log the interaction details
        logging.info(f'Processed interaction: Text: "{text}" -> Response: "{response}"')

    def log_error(self, message):
        # Log any errors that occur
        logging.error(message)

    def log_info(self, message):
        # Log general information
        logging.info(message)

if __name__ == "__main__":
    # Example usage of logging functions
    logger = CustomLogger("system_logs.log")
    logger.log_interaction("Hello", "Hi there!")
    logger.log_error("This is an error message.")
    logger.log_info("This is a general information message.")