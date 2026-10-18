
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from app.agents.workflow import support_graph


app = FastAPI(
    title="NexaCare Customer Support API",
    description=(
        "An AI-powered customer support API "
        "with RAG and human-review governance."
    ),
    version="1.0.0",
)


class SupportRequest(BaseModel):
    customer_question: str = Field(
        ...,
        min_length=1,
        max_length=5000,
        description="The customer's support question.",
    )


@app.get("/health")
def health_check() -> dict:
    """Check whether the API is running."""
    return {
        "status": "healthy",
        "service": "NexaCare Customer Support API",
    }


@app.post("/support")
def handle_support_request(request: SupportRequest) -> dict:
    """Run the customer-support agent workflow."""
    question = request.customer_question.strip()

    if not question:
        raise HTTPException(
            status_code=422,
            detail="Customer question cannot be empty.",
        )

    try:
        result = support_graph.invoke(
            {"customer_question": question}
        )

        return {
            "customer_question": question,
            "intent": result.get("intent", ""),
            "sentiment": result.get("sentiment", ""),
            "urgency": result.get("urgency", ""),
            "response": result.get("response", ""),
            "sources": result.get("sources", []),
            "requires_human_review": result.get(
                "requires_human_review", False
            ),
            "escalation_reason": result.get(
                "escalation_reason", ""
            ),
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="The support workflow failed.",
        ) from exc
