from transformers import pipeline, AutoModelForSequenceClassification, AutoTokenizer, AutoModelForSeq2SeqLM
import logging

class MLModel:
    def __init__(self, logger):
        self.logger = logger
        # Initialize the sentiment analysis model
        model_name_sentiment = "distilbert-base-uncased-finetuned-sst-2-english"
        tokenizer_sentiment = AutoTokenizer.from_pretrained(model_name_sentiment)
        model_sentiment = AutoModelForSequenceClassification.from_pretrained(model_name_sentiment)
        self.sentiment_analyzer = pipeline('sentiment-analysis', model=model_sentiment, tokenizer=tokenizer_sentiment)

        # Initialize the summarization model
        model_name_summarization = "facebook/bart-large-cnn"
        tokenizer_summarization = AutoTokenizer.from_pretrained(model_name_summarization)
        model_summarization = AutoModelForSeq2SeqLM.from_pretrained(model_name_summarization)
        self.summarizer = pipeline('summarization', model=model_summarization, tokenizer=tokenizer_summarization)

    def analyze_sentiment(self, text):
        try:
            result = self.sentiment_analyzer(text)
            score = result[0]['score']
            label = result[0]['label']
            if label == 'NEGATIVE':
                score = -score
            return score
        except Exception as e:
            self.logger.log_error(f"Error in sentiment analysis: {e}")
            return 0  # Neutral sentiment in case of error

    def summarize_text(self, text):
        try:
            result = self.summarizer(text, max_length=130, min_length=30, do_sample=False)
            return result[0]['summary_text']
        except Exception as e:
            self.logger.log_error(f"Error in text summarization: {e}")
            return text  # Return original text if summarization fails

if __name__ == "__main__":
    from custom_logger import CustomLogger  # Assuming CustomLogger is in custom_logger.py
    # Generate or retrieve an existing encryption key
    key = Fernet.generate_key()  # In practice, use a secure method to manage this key
    logger = CustomLogger("secure_system_logs.log", encryption_key=key)
    ml_model = MLModel(logger)
    text = "The quick brown fox jumps over the lazy dog. This story is about how quick movements can be beneficial in some scenarios."
    logger.log_info("Sentiment Analysis Result: " + str(ml_model.analyze_sentiment(text)))
    logger.log_info("Text Summarization Result: " + str(ml_model.summarize_text(text)))