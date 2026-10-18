
from app.agents.state import SupportState


def assess_escalation(state: SupportState) -> dict:
    """
    Apply explicit governance rules to determine whether
    a customer request requires human review.

    This node does not approve refunds or make financial decisions.
    """

    question = state["customer_question"].lower()
    intent = state.get("intent", "unknown")
    sentiment = state.get("sentiment", "neutral")
    urgency = state.get("urgency", "normal")

    requires_human_review = False
    escalation_reason = ""

    # Rule 1: Financial disputes and duplicate charges
    financial_dispute_phrases = [
        "charged twice",
        "duplicate charge",
        "wrong charge",
        "incorrect charge",
        "billing dispute",
        "dispute a payment",
        "unauthorised payment",
        "unauthorized payment",
    ]

    if any(phrase in question for phrase in financial_dispute_phrases):
        requires_human_review = True
        escalation_reason = (
            "Financial dispute or possible duplicate charge "
            "requires human review."
        )

    # Rule 2: Refund approval or guarantee requests
    refund_decision_phrases = [
        "approve my refund",
        "guarantee my refund",
        "confirm my refund is approved",
        "when will you approve my refund",
    ]

    if any(phrase in question for phrase in refund_decision_phrases):
        requires_human_review = True
        escalation_reason = (
            "Refund approval must be reviewed by an authorised human."
        )

    # Rule 3: Delivery disputes
    if any(
        phrase in question
        for phrase in [
            "delivered but not received",
            "marked as delivered but not received",
            "package never arrived",
            "delivery dispute",
        ]
    ):
        requires_human_review = True
        escalation_reason = (
            "Delivery dispute requires investigation by a human."
        )

    # Rule 4: Urgent or high-impact cases
    if urgency == "high" and (
        intent in {"billing", "complaint", "shipping"}
        or sentiment == "negative"
    ):
        requires_human_review = True
        escalation_reason = (
            "Urgent customer issue requires human assessment."
        )

    # Rule 5: Complaints requiring formal investigation
    if intent == "complaint":
        requires_human_review = True
        escalation_reason = (
            "Customer complaint requires human assessment."
        )

    return {
        "requires_human_review": requires_human_review,
        "escalation_reason": escalation_reason,
    }


def generate_response_node(state: SupportState) -> dict:
    """Generate a grounded response using retrieved knowledge."""

    if state.get("requires_human_review", False):
        reason = state.get(
            "escalation_reason",
            "This request requires additional review.",
        )

        return {
            "response": (
                "Thank you for contacting NexaCare. "
                "Your request needs to be reviewed by our support team. "
                f"Reason: {reason} "
                "A support representative will review your case."
            )
        }

    context = state.get("retrieved_context", [])

    if not context:
        return {
            "response": (
                "Thank you for contacting NexaCare. "
                "I couldn't find enough information in our approved "
                "support documentation to answer confidently. "
                "Please contact our support team for further assistance."
            )
        }

    relevant_information = "\n\n".join(context)

    return {
        "response": (
            "Thank you for contacting NexaCare. "
            "I found the following information in our support documentation:\n\n"
            f"{relevant_information}\n\n"
            "If this doesn't resolve your question, please contact "
            "our support team for further assistance."
        )
    }
