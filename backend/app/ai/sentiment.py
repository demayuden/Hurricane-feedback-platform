def analyze_sentiment(text: str) -> str:
    # Temporary placeholder (no ML dependency)
    text = text.lower()
    if any(word in text for word in ["stress", "too much", "overload", "burnout"]):
        return "NEGATIVE"
    if any(word in text for word in ["good", "happy", "great", "satisfied"]):
        return "POSITIVE"
    return "NEUTRAL"
