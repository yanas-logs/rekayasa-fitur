import re
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from deep_translator import GoogleTranslator

nltk.download('vader_lexicon', quiet=True)
vader = SentimentIntensityAnalyzer()

def clean_and_translate(text):
    try:
        clean_text = re.sub(r"http\S+|[^a-zA-Z0-9\s.,!?]", '', str(text))
        if not clean_text.strip(): return None
        return GoogleTranslator(source='auto', target='en').translate(clean_text)
    except:
        return None

def get_sentiment(text):
    translated = clean_and_translate(text)
    if not translated: return 'Neutral'
    scores = vader.polarity_scores(translated)
    if scores['compound'] >= 0.05: return 'Positive'
    elif scores['compound'] <= -0.05: return 'Negative'
    else: return 'Neutral'