
from app.agents.state import SupportState


def analyse_sentiment_urgency(state: SupportState) -> dict:
    """Apply transparent baseline rules to assess tone and urgency."""

    question = state["customer_question"].lower()

    negative_phrases = [
        "angry", "frustrated", "furious", "terrible",
        "unacceptable", "disappointed", "unhappy",
        "fed up", "awful", "ridiculous"
    ]

    positive_phrases = [
        "thank you", "thanks", "great service",
        "happy", "excellent", "appreciate"
    ]

    urgent_phrases = [
        "urgent", "urgently", "immediately", "asap",
        "emergency", "locked out", "fraud",
        "charged twice", "cannot access"
    ]

    if any(phrase in question for phrase in negative_phrases):
        sentiment = "negative"
    elif any(phrase in question for phrase in positive_phrases):
        sentiment = "positive"
    else:
        sentiment = "neutral"

    if any(phrase in question for phrase in urgent_phrases):
        urgency = "high"
    else:
        urgency = "normal"

    return {
        "sentiment": sentiment,
        "urgency": urgency,
    }