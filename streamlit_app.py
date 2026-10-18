import os
import requests
import streamlit as st

# --------------------------------------------------
# NexaCare Customer Support Interface
# --------------------------------------------------

API_URL = "http://127.0.0.1:8001/support"
API_URL = os.getenv("API_URL", API_URL)

st.set_page_config(
    page_title="NexaCare Customer Support",
    page_icon="💬",
    layout="centered",
)

st.title("💬 NexaCare Customer Support")
st.caption(
    "AI-powered customer support with approved knowledge "
    "retrieval and human-review safeguards."
)

st.divider()

st.subheader("How can we help you?")
st.write(
    "Enter your question below. Our support system will "
    "search its approved documentation and determine "
    "whether your request needs human review."
)

with st.form("support_form", clear_on_submit=False):
    customer_question = st.text_area(
        "Your question",
        placeholder=(
            "Example: I was charged twice for my order."
        ),
        max_chars=5000,
        height=130,
    )

    submitted = st.form_submit_button(
        "Submit support request",
        type="primary",
        use_container_width=True,
    )

if submitted:
    question = customer_question.strip()

    if not question:
        st.warning("Please enter your question first.")

    else:
        with st.spinner(
            "Analysing your request and searching approved documentation..."
        ):
            try:
                response = requests.post(
                    API_URL,
                    json={"customer_question": question},
                    timeout=120,
                )

                if response.status_code == 200:
                    result = response.json()

                    st.success("Your support request has been processed.")

                    st.subheader("Support response")
                    st.write(
                        result.get(
                            "response",
                            "No response was returned.",
                        )
                    )

                    col1, col2 = st.columns(2)

                    with col1:
                        st.metric(
                            "Intent",
                            result.get("intent") or "Unknown",
                        )

                    with col2:
                        st.metric(
                            "Urgency",
                            result.get("urgency") or "Unknown",
                        )

                    sentiment = result.get(
                        "sentiment", "Unknown"
                    )
                    st.write(f"**Sentiment:** {sentiment}")

                    if result.get("requires_human_review", False):
                        st.warning(
                            "Human review required. "
                            "Your request needs attention from "
                            "a support representative."
                        )

                        reason = result.get("escalation_reason")
                        if reason:
                            st.write(f"**Reason:** {reason}")

                    else:
                        st.info(
                            "This request was not flagged for "
                            "human review by the current rules."
                        )

                    sources = result.get("sources", [])

                    with st.expander(
                        "View supporting documents",
                        expanded=False,
                    ):
                        if sources:
                            for source in dict.fromkeys(sources):
                                st.write(f"- {source}")
                        else:
                            st.write(
                                "No source documents were returned."
                            )

                    with st.expander(
                        "View request details",
                        expanded=False,
                    ):
                        st.json(result)

                else:
                    st.error(
                        f"The support API returned HTTP "
                        f"{response.status_code}."
                    )

                    try:
                        st.write(response.json())
                    except ValueError:
                        st.write(response.text)

            except requests.exceptions.ConnectionError:
                st.error(
                    "Could not connect to the support API. "
                    "Make sure your FastAPI server is running "
                    "on port 8001."
                )

            except requests.exceptions.Timeout:
                st.error(
                    "The request took too long. Please try again."
                )

            except requests.exceptions.RequestException as exc:
                st.error(f"Request failed: {exc}")

st.divider()

st.caption(
    "NexaCare AI Support | Responses are based on retrieved "
    "documentation. Financial decisions, complaints, and other "
    "flagged cases may require human review."
)