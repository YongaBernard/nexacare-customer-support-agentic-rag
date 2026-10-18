
from app.agents.escalation import assess_escalation


def test_duplicate_charge_requires_human_review():
    state = {
        "customer_question": "I was charged twice for my order",
        "intent": "billing",
        "sentiment": "neutral",
        "urgency": "high",
    }

    result = assess_escalation(state)

    assert result["requires_human_review"] is True
    assert result["escalation_reason"] != ""


def test_complaint_requires_human_review():
    state = {
        "customer_question": "I want to make a complaint",
        "intent": "complaint",
        "sentiment": "neutral",
        "urgency": "normal",
    }

    result = assess_escalation(state)

    assert result["requires_human_review"] is True
    assert result["escalation_reason"] != ""


def test_normal_delivery_question_does_not_require_review():
    state = {
        "customer_question": "Where is my delivery?",
        "intent": "shipping",
        "sentiment": "neutral",
        "urgency": "normal",
    }

    result = assess_escalation(state)

    assert result["requires_human_review"] is False
    assert result["escalation_reason"] == ""
