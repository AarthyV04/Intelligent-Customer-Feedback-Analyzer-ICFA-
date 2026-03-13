from transformers import pipeline
import nltk
from collections import Counter
import re

nltk.download("stopwords", quiet=True)
from nltk.corpus import stopwords

print("Loading HuggingFace DistilBERT sentiment model...")
sentiment_pipeline = pipeline(
    "sentiment-analysis",
    model="distilbert-base-uncased-finetuned-sst-2-english"
)
print("Sentiment model ready!")

STOP_WORDS = set(stopwords.words("english"))


def analyze_sentiment(text: str) -> dict:
    """Returns label (POSITIVE/NEGATIVE/NEUTRAL) and confidence score."""
    try:
        result = sentiment_pipeline(text[:512])[0]
        label = result["label"]
        # Treat low-confidence results as NEUTRAL
        if result["score"] < 0.65:
            label = "NEUTRAL"
        return {"label": label, "score": round(result["score"], 3)}
    except Exception as e:
        print(f"Sentiment error: {e}")
        return {"label": "NEUTRAL", "score": 0.5}


def extract_keywords(texts: list, top_n: int = 15) -> list:
    """Extract most frequent meaningful words from a list of texts."""
    all_words = []
    for text in texts:
        words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
        words = [w for w in words if w not in STOP_WORDS]
        all_words.extend(words)
    counter = Counter(all_words)
    return [{"word": w, "count": c} for w, c in counter.most_common(top_n)]
