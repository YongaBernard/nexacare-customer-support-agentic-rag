# NexaCare Customer Support Agentic RAG System

An AI-powered customer-support application built with **Python, FastAPI, LangGraph, ChromaDB, and Streamlit**, featuring retrieval-augmented generation (RAG), customer-intent analysis, sentiment and urgency assessment, and human-review governance.

## Project Overview

NexaCare is a customer-support prototype designed to retrieve information from approved support documentation and help handle common customer questions.

The application combines a LangGraph workflow with a FastAPI backend and a Streamlit interface. It also includes explicit governance rules to flag complaints, billing disputes, and other cases requiring human assessment.

## Key Features

- **Retrieval-Augmented Generation (RAG):** Retrieves relevant information from a local knowledge base.
- **Semantic search:** Uses Sentence Transformers embeddings with ChromaDB.
- **Intent classification:** Categorises customer requests, including shipping, billing, refunds, and complaints.
- **Sentiment and urgency analysis:** Assesses customer sentiment and urgency.
- **Human-review governance:** Flags requests that require assessment by an authorised support representative.
- **REST API:** Exposes the support workflow through FastAPI.
- **Interactive interface:** Allows users to submit questions and inspect responses, supporting documents, and request metadata through Streamlit.
- **Automated tests:** Includes tests for workflow behaviour and escalation rules.
- **Local development:** Supports running the application locally without deploying it to AWS.

## Architecture

```text
Customer
   |
   v
Streamlit User Interface
   |
   v
FastAPI Support API
   |
   v
LangGraph Workflow
   |
   +--> Intent Detection
   |
   +--> Sentiment and Urgency Analysis
   |
   +--> ChromaDB Knowledge Retrieval
   |       |
   |       v
   |   Sentence Transformers Embeddings
   |
   +--> Escalation and Governance
   |
   +--> Response Generation
           |
           v
      Structured API Response
```

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application development |
| FastAPI | REST API |
| LangGraph | Workflow orchestration |
| ChromaDB | Vector database |
| Sentence Transformers | Local text embeddings |
| LangChain integrations | Vector-store and embedding interfaces |
| Streamlit | Customer-facing interface |
| Pydantic | API request validation |
| Pytest | Automated testing |

## Project Structure

```text
customer-support-agentic-rag/
├── app/
│   ├── agents/
│   │   ├── escalation.py
│   │   ├── intent_detector.py
│   │   ├── sentiment_urgency.py
│   │   ├── state.py
│   │   └── workflow.py
│   ├── rag/
│   │   ├── ingest.py
│   │   └── retriever.py
│   └── main.py
├── data/
├── governance/
├── notebooks/
├── tests/
│   ├── test_escalation.py
│   └── test_workflow.py
├── streamlit_app.py
├── requirements.txt
├── pytest.ini
├── .gitignore
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.11 or a compatible Python version.
- pip.
- A terminal and a code editor such as Visual Studio Code.

### 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd customer-support-agentic-rag
```

Replace the placeholder with your repository URL.

### 2. Create and activate a virtual environment

On macOS or Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Prepare the knowledge base

The application uses approved support documents and a local ChromaDB collection. Populate the local vector database using the ingestion workflow in `app/rag/ingest.py` before querying if the database has not already been created.

### 5. Run the automated tests

```bash
pytest -q
```

The current development baseline is **7 passing tests**.

### 6. Start the FastAPI backend

```bash
uvicorn app.main:app --host 127.0.0.1 --port 8001 --reload
```

API documentation:

- Swagger UI: http://127.0.0.1:8001/docs
- Health endpoint: http://127.0.0.1:8001/health

### 7. Start the Streamlit interface

Open a second terminal, activate the virtual environment, and run:

```bash
streamlit run streamlit_app.py
```

Open the local URL printed by Streamlit, usually http://localhost:8501.

Keep both the FastAPI and Streamlit processes running while using the application.

## API Usage

### Health Check

**Endpoint:** `GET /health`

Example response:

```json
{
  "status": "healthy",
  "service": "NexaCare Customer Support API"
}
```

### Submit a Support Request

**Endpoint:** `POST /support`

Example request:

```json
{
  "customer_question": "Where is my delivery?"
}
```

The response includes fields for:

- The original customer question.
- Predicted intent, sentiment, and urgency.
- The support response.
- Retrieved source filenames.
- Human-review status.
- Escalation reason.

## Human-Review Governance

The escalation rules identify cases that may require human assessment, including:

- Potential duplicate charges and financial disputes.
- Refund approval or guarantee requests.
- Customer complaints.
- Delivery disputes.
- Urgent or high-impact support issues.

The application is designed not to independently approve refunds, guarantee delivery dates, or make unsupported commitments.

Flagging a request for review does not itself create a ticket or notify a human agent. Those capabilities would require a further integration.

## Testing

Run the complete test suite:

```bash
pytest -q
```

The existing tests cover workflow behaviour and escalation scenarios. Additional integration, retrieval-quality, API validation, and user-interface tests can strengthen the test suite as development continues.

## Current Implementation Status

The local prototype has a working FastAPI backend, a LangGraph workflow, local vector retrieval, a Streamlit interface, and human-review rules. The current response-generation component formats retrieved policy content and uses predefined escalation messages; it does not yet use an LLM to summarise retrieved content into consistently concise, conversational answers.

The system has been tested locally with shipping, billing-dispute, refund, and complaint scenarios.

## Security and Limitations

- Do not commit `.env` files, API keys, credentials, or private customer data.
- Keep generated local databases and environment-specific files out of version control when they can be recreated.
- Validate retrieved answers and escalation decisions against additional test cases before production use.
- A live order-status lookup, ticket creation, human-agent notification, authentication, authorisation, and production monitoring are not yet implemented.
- The current local prototype does not require AWS deployment.

## Future Development

Planned enhancements include:

- Improved retrieval ranking and duplicate-content handling.
- LLM-based grounded response generation.
- More comprehensive automated tests.
- Ticket-management and order-management integrations.
- Authentication, observability, and production hardening.
- Optional AWS deployment.

## Author

Developed as a practical portfolio project demonstrating RAG, AI workflow orchestration, API engineering, and human-in-the-loop governance.
