from app.agents.workflow import support_graph


def run_workflow(question: str) -> dict:
    """Run the complete customer support workflow."""
    return support_graph.invoke({
        "customer_question": question
    })


def test_delivery_question_retrieves_knowledge():
    result = run_workflow("Where is my delivery?")

    assert result["intent"] == "shipping"
    assert len(result["retrieved_context"]) > 0
    assert len(result["sources"]) > 0


def test_duplicate_charge_requires_human_review():
    result = run_workflow("I was charged twice for my order")

    assert result["intent"] == "billing"
    assert result["requires_human_review"] is True
    assert result["escalation_reason"] != ""


def test_complaint_requires_human_review():
    result = run_workflow("I want to make a complaint")

    assert result["intent"] == "complaint"
    assert result["requires_human_review"] is True


def test_positive_feedback_does_not_require_review():
    result = run_workflow("Thank you for the excellent service")

    assert result["sentiment"] == "positive"
    assert result["requires_human_review"] is False
