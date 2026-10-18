
from app.agents.state import SupportState


def detect_intent(state: SupportState) -> dict:
    """Classify a customer question using transparent keyword rules."""

    question = state["customer_question"].lower()

    intent_keywords = {
        "refund": [
            "refund", "return", "returned", "money back",
            "exchange", "reimbursement"
        ],
        "billing": [
            "payment", "charged", "charge", "invoice",
            "billing", "bill", "duplicate charge", "overcharged"
        ],
        "shipping": [
            "shipping", "delivery", "delivered", "parcel",
            "package", "tracking", "order status", "shipment"
        ],
        "account": [
            "account", "login", "log in", "password",
            "sign in", "profile", "locked out"
        ],
        "complaint": [
            "complaint", "complain", "unhappy", "frustrated",
            "terrible service", "poor service", "unacceptable"
        ],
    }

    scores = {
        intent: sum(
            1 for keyword in keywords if keyword in question
        )
        for intent, keywords in intent_keywords.items()
    }

    highest_score = max(scores.values())

    if highest_score == 0:
        detected_intent = "unknown"
    else:
        # Resolve ties deterministically using the category order above.
        detected_intent = next(
            intent
            for intent, score in scores.items()
            if score == highest_score
        )

    return {"intent": detected_intent}