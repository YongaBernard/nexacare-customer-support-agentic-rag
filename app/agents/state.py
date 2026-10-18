
from typing import TypedDict, List


class SupportState(TypedDict):
    # Customer input
    customer_question: str

    # Customer analysis
    intent: str
    sentiment: str
    urgency: str

    # Knowledge retrieval
    retrieved_context: List[str]
    sources: List[str]

    # Governance and safety
    requires_human_review: bool
    escalation_reason: str

    # Final output
    response: str