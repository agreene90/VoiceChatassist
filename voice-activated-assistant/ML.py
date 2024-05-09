from transformers import pipeline, AutoModelForSequenceClassification, AutoTokenizer, AutoModelForSeq2SeqLM

class MLModel:
    def __init__(self):
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
        """ Analyze sentiment of the given text, returning a score from -1 (negative) to 1 (positive). """
        try:
            result = self.sentiment_analyzer(text)
            score = result[0]['score']
            label = result[0]['label']
            if label == 'NEGATIVE':
                score = -score
            return score
        except Exception as e:
            print(f"Error in sentiment analysis: {e}")
            return 0  # Neutral sentiment in case of error

    def summarize_text(self, text):
        """ Summarize the given text and return the summarized version. """
        try:
            result = self.summarizer(text, max_length=130, min_length=30, do_sample=False)
            return result[0]['summary_text']
        except Exception as e:
            print(f"Error in text summarization: {e}")
            return text  # Return original text if summarization fails

# Example usage of the MLModel class
if __name__ == "__main__":
    ml_model = MLModel()
    text = "The quick brown fox jumps over the lazy dog. This story is about how quick movements can be beneficial in some scenarios."
    print("Sentiment Analysis Result:", ml_model.analyze_sentiment(text))
    print("Text Summarization Result:", ml_model.summarize_text(text))