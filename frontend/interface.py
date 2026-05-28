"""Streamlit frontend for the banking service."""

from __future__ import annotations

import os

import requests
import streamlit as st


API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")


st.set_page_config(page_title="Banking Service", page_icon="🏦", layout="wide")

st.markdown(
    """
    <style>
        .stApp {
            background: linear-gradient(135deg, #f6efe7 0%, #eef3f8 45%, #ffffff 100%);
        }
        .hero {
            padding: 1.25rem 1.5rem;
            border-radius: 1.2rem;
            background: rgba(255, 255, 255, 0.82);
            border: 1px solid rgba(60, 60, 60, 0.08);
            box-shadow: 0 18px 40px rgba(0, 0, 0, 0.06);
            margin-bottom: 1rem;
        }
        .hero h1 {
            margin: 0;
            font-size: 2.2rem;
        }
        .hero p {
            margin: 0.35rem 0 0;
            color: #4d5562;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero">
        <h1>Banking Service Frontend</h1>
        <p>Send a customer message to the API Gateway and inspect the full agentic workflow trace.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.header("Gateway")
    st.write(API_BASE_URL)
    st.caption("The frontend calls POST /run-agent on the backend service.")
    st.divider()
    st.caption("Microservices")
    st.write("• backend")
    st.write("• intent-service")
    st.write("• Ollama endpoint (external)")

message = st.text_area(
    "Customer message",
    placeholder="Example: My card payment was declined at the supermarket yesterday.",
    height=180,
)

col_left, col_right = st.columns([1, 1])
with col_left:
    run_clicked = st.button("Run agent", use_container_width=True)
with col_right:
    st.button("Clear", use_container_width=True, on_click=lambda: st.session_state.update({"_clear": True}))

if run_clicked:
    if not message.strip():
        st.error("Please enter a customer message first.")
    else:
        with st.spinner("Running the agent workflow..."):
            try:
                response = requests.post(
                    f"{API_BASE_URL.rstrip('/')}/run-agent",
                    json={"message": message},
                    timeout=120,
                )
                response.raise_for_status()
                result = response.json()
            except Exception as exc:
                st.error(f"Could not reach the API Gateway: {exc}")
            else:
                st.subheader("Final reply")
                st.success(result["final_reply"])

                left, right = st.columns(2)
                with left:
                    st.markdown("### Intent")
                    st.json(result["intent"])
                    st.markdown("### Priority")
                    st.json(result["priority"])
                with right:
                    st.markdown("### Policy")
                    st.json(result["policy"])
                    st.markdown("### Routing")
                    st.json(result["routing"])

                with st.expander("Draft and validation"):
                    st.json(result["draft"])
                    st.json(result["validation"])
