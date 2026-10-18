
from typing import Any

from langgraph.graph import StateGraph, START, END

from app.agents.state import SupportState
from app.agents.intent_detector import detect_intent
from app.agents.sentiment_urgency import analyse_sentiment_urgency
from app.agents.escalation import (
    assess_escalation,
    generate_response_node,
)

from app.rag.retriever import retrieve_documents



def retrieve_knowledge(state: SupportState) -> dict:
    """Retrieve relevant approved knowledge for the customer question."""
    documents = retrieve_documents(
        query=state["customer_question"],
        k=4,
    )

    sources = list(
        dict.fromkeys(
            document.metadata.get("source", "unknown")
            for document in documents
        )
    )

    return {
        "retrieved_context": [
            document.page_content for document in documents
        ],
        "sources": sources,
    }


def assess_escalation_node(state: SupportState) -> dict:
    """Apply escalation and human-review governance rules."""
    return assess_escalation(state)


def build_support_graph() -> Any:
    """Build the initial customer-support analysis workflow."""

    graph = StateGraph(SupportState)

    # Register workflow nodes
    graph.add_node("detect_intent", detect_intent)
    graph.add_node("analyse_sentiment_urgency", analyse_sentiment_urgency)
    graph.add_node("retrieve_knowledge", retrieve_knowledge)
    graph.add_node("assess_escalation", assess_escalation_node)
    graph.add_node("generate_response", generate_response_node)
    # Connect nodes in execution order
    graph.add_edge(START, "detect_intent")
    graph.add_edge("detect_intent", "analyse_sentiment_urgency")
    graph.add_edge("analyse_sentiment_urgency", "retrieve_knowledge")
    graph.add_edge("retrieve_knowledge", "assess_escalation")
    graph.add_edge("assess_escalation", "generate_response")
    graph.add_edge("generate_response", END)

    return graph.compile()


support_graph = build_support_graph()