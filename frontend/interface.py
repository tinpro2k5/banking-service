"""Streamlit frontend for the banking service."""

from __future__ import annotations

import html
import json
import os

import requests
import streamlit as st


API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")


DEMO_MESSAGES = [
    {
        "label": "💸 Transfer not received",
        "message": "I made a transfer 3 days ago but the recipient hasn't received the money.",
        "badge": "ask_more",
    },
    {
        "label": "🚫 Card blocked",
        "message": "My card was blocked and I can't make any payments.",
        "badge": "escalate",
    },
    {
        "label": "⚠️ Unauthorized payment",
        "message": "Someone made an unauthorized card payment of $79.40 on my account ending 4432 yesterday.",
        "badge": "escalate",
    },
    {
        "label": "📦 Refund missing",
        "message": "I returned the product on 2026-05-02 and my refund for order 771245 still has not shown up in my account number 1234.",
        "badge": "reply",
    },
    {
        "label": "💰 Check balance",
        "message": "How do I check my account balance.",
        "badge": "reply",
    },
    {
        "label": "❓ Unknown issue",
        "message": "My grandmother's account keeps making beeping sounds.",
        "badge": "ask_more",
    },
]

BADGE_COLORS = {
    "reply":    ("#dcfce7", "#15803d"),
    "escalate": ("#fee2e2", "#b91c1c"),
    "ask_more": ("#fef9c3", "#854d0e"),
}


def clear_message() -> None:
    st.session_state["message_input"] = ""


def set_message(text: str) -> None:
    st.session_state["message_input"] = text


st.set_page_config(page_title="Banking Service", page_icon="🏦", layout="wide")

st.markdown(
    """
    <style>
        .stApp,
        .stApp [data-testid="stAppViewContainer"] {
            color: #152033;
        }
        .stApp {
            background: linear-gradient(135deg, #f6efe7 0%, #eef3f8 45%, #ffffff 100%);
        }
        section[data-testid="stSidebar"],
        section[data-testid="stSidebar"] > div,
        section[data-testid="stSidebar"] [data-testid="stSidebarContent"] {
            background: #f8fafc !important;
            color: #152033 !important;
        }
        section[data-testid="stSidebar"] *,
        section[data-testid="stSidebar"] h1,
        section[data-testid="stSidebar"] h2,
        section[data-testid="stSidebar"] h3,
        section[data-testid="stSidebar"] h4,
        section[data-testid="stSidebar"] h5,
        section[data-testid="stSidebar"] h6,
        section[data-testid="stSidebar"] p,
        section[data-testid="stSidebar"] span,
        section[data-testid="stSidebar"] label,
        section[data-testid="stSidebar"] button,
        section[data-testid="stSidebar"] a,
        section[data-testid="stSidebar"] svg {
            color: #152033 !important;
            fill: #152033 !important;
        }
        section[data-testid="stSidebar"] a {
            color: #0f766e !important;
        }
        section[data-testid="stSidebar"] hr,
        section[data-testid="stSidebar"] [data-testid="stDivider"] {
            border-color: rgba(21, 32, 51, 0.14) !important;
        }
        .hero {
            padding: 1.25rem 1.5rem;
            border-radius: 1.2rem;
            background: rgba(255, 255, 255, 0.82);
            border: 1px solid rgba(60, 60, 60, 0.08);
            box-shadow: 0 18px 40px rgba(0, 0, 0, 0.06);
            margin-bottom: 1rem;
            color: #152033;
        }
        .hero h1 {
            margin: 0;
            font-size: 2.2rem;
            color: #152033 !important;
        }
        .hero p {
            margin: 0.35rem 0 0;
            color: #4d5562;
        }
        div[data-testid="stAppViewContainer"] div[data-testid="stMarkdownContainer"] h1,
        div[data-testid="stAppViewContainer"] div[data-testid="stMarkdownContainer"] h2,
        div[data-testid="stAppViewContainer"] div[data-testid="stMarkdownContainer"] h3,
        div[data-testid="stAppViewContainer"] div[data-testid="stMarkdownContainer"] h4,
        div[data-testid="stAppViewContainer"] div[data-testid="stMarkdownContainer"] h5,
        div[data-testid="stAppViewContainer"] div[data-testid="stMarkdownContainer"] h6,
        div[data-testid="stAppViewContainer"] div[data-testid="stMarkdownContainer"] p,
        div[data-testid="stAppViewContainer"] div[data-testid="stTextArea"] label,
        div[data-testid="stAppViewContainer"] div[data-testid="stTextArea"] label * {
            color: #152033 !important;
        }
        div[data-testid="stTextArea"] textarea {
            background: #ffffff !important;
            color: #152033 !important;
            caret-color: #152033 !important;
            border: 1px solid rgba(21, 32, 51, 0.18) !important;
            box-shadow: inset 0 1px 2px rgba(15, 23, 42, 0.04);
        }
        div[data-testid="stTextArea"] textarea:focus,
        div[data-testid="stTextArea"] textarea:focus-visible {
            caret-color: #152033 !important;
            outline: 2px solid rgba(21, 32, 51, 0.22) !important;
            outline-offset: 2px;
        }
        div[data-testid="stTextArea"] textarea::placeholder {
            color: #6b7280 !important;
            opacity: 1;
        }
        div[data-testid="stButton"] > button {
            background: linear-gradient(135deg, #f59e0b 0%, #f97316 100%) !important;
            color: #ffffff !important;
            border: 0 !important;
            border-radius: 0.8rem !important;
            box-shadow: 0 10px 24px rgba(249, 115, 22, 0.22);
        }
        div[data-testid="stButton"] > button:hover {
            filter: brightness(1.03);
            box-shadow: 0 12px 28px rgba(249, 115, 22, 0.28);
        }
        div[data-testid="stButton"] > button:focus-visible {
            outline: 3px solid rgba(245, 158, 11, 0.35);
            outline-offset: 2px;
        }
          /* Result cards: cleaner layout and lighter tones */
          .results-grid {
              display: grid;
              grid-template-columns: 1fr;
              gap: 1.25rem;
              align-items: start;
              margin: 0.5rem 0 1.25rem !important;
          }
          .result-card {
              background: #ffffff;
              border: 1px solid rgba(15, 23, 42, 0.08);
              border-radius: 0.9rem;
              padding: 0.85rem 1rem 0.9rem;
              box-shadow: 0 10px 28px rgba(15, 23, 42, 0.08);
              overflow: hidden;
          }
          .result-card .card-title {
              font-size: 1.05rem;
              font-weight: 600;
              color: #0f172a;
              margin: 0.1rem 0 0.6rem;
          }
          .result-card pre {
              margin: 0;
              font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, 'Roboto Mono', 'Segoe UI Mono', monospace;
              font-size: 13px;
              line-height: 1.55;
              color: #1f2937;
              background: #f5f7fb;
              border-radius: 0.6rem;
              padding: 0.75rem 0.85rem;
              border: 1px solid rgba(148, 163, 184, 0.35);
              overflow: auto;
              white-space: pre-wrap;
              word-break: break-word;
          }
          .result-card code {
              color: inherit;
              background: transparent;
          }
          /* Draft and Validation: full-width cards stacked below grid */
          .results-wide {
              display: grid;
              grid-template-columns: 1fr;
              gap: 1rem;
              margin: 0 0 1.25rem !important;
          }
        /* Reduce the overly large dark bars (expander headers / dividers) */
        .streamlit-expanderHeader, div[data-testid="stDivider"] {
              background: transparent !important;
              height: auto !important;
              border-radius: 0.25rem !important;
              margin: 0.45rem 0 !important;
              border: none !important;
        }
        /* Headings spacing */
        div[data-testid="stAppViewContainer"] h1,
        div[data-testid="stAppViewContainer"] h2,
        div[data-testid="stAppViewContainer"] h3 {
              margin-top: 0.9rem !important;
              margin-bottom: 0.7rem !important;
              color: #0b1720 !important;
        }
        /* Make the sidebar text clearer */
        section[data-testid="stSidebar"] {
            font-family: Inter, system-ui, -apple-system, 'Segoe UI', Roboto, 'Helvetica Neue', Arial !important;
            font-size: 15px !important;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


def render_result_card(title: str, payload: object) -> str:
    pretty = json.dumps(payload, indent=2, ensure_ascii=False)
    safe_payload = html.escape(pretty)
    safe_title = html.escape(title)
    return (
        f"<div class=\"result-card\">"
        f"<div class=\"card-title\">{safe_title}</div>"
        f"<pre><code>{safe_payload}</code></pre>"
        f"</div>"
    )

st.markdown(
    """
    <div class="hero">
        <h1 style="margin: 0; font-size: 2.2rem; color: #152033;">Banking Service Frontend</h1>
        <p style="margin: 0.35rem 0 0; color: #4d5562;">Send a customer message to the API Gateway and inspect the full agentic workflow trace.</p>
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
    st.divider()
    st.markdown(
        """
        <div style="font-size:0.92rem; font-weight:700; color:#0f172a;
                    margin-bottom:0.5rem; letter-spacing:0.01em;">
            ⚡ Quick Demo
        </div>
        <div style="font-size:0.78rem; color:#6b7280; margin-bottom:0.75rem;">
            Click a message to load it instantly.
        </div>
        """,
        unsafe_allow_html=True,
    )
    for demo in DEMO_MESSAGES:
        bg, fg = BADGE_COLORS.get(demo["badge"], ("#f3f4f6", "#374151"))
        st.markdown(
            f"""
            <div style="display:flex; align-items:center; gap:0.4rem;
                        margin-bottom:0.15rem;">
                <span style="background:{bg}; color:{fg}; font-size:0.68rem;
                             font-weight:700; padding:0.1rem 0.45rem;
                             border-radius:999px; white-space:nowrap;">
                    {demo['badge']}
                </span>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.button(
            demo["label"],
            key=f"demo_{demo['label']}",
            use_container_width=True,
            on_click=set_message,
            args=(demo["message"],),
        )

st.markdown(
    '<div style="margin: 0.25rem 0 0.35rem; color: #152033; font-weight: 600;">Customer message</div>',
    unsafe_allow_html=True,
)

message = st.text_area(
    "Customer message",
    label_visibility="collapsed",
    placeholder="Example: My card payment was declined at the supermarket yesterday.",
    height=180,
    key="message_input",
)

col_left, col_right = st.columns([1, 1])
with col_left:
    run_clicked = st.button("Run agent", use_container_width=True)
with col_right:
    st.button("Clear", use_container_width=True, on_click=clear_message)

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

                cards = [
                    render_result_card("Intent", result["intent"]),
                    render_result_card("Policy", result["policy"]),
                    render_result_card("Priority", result["priority"]),
                    render_result_card("Routing", result["routing"]),
                ]
                st.markdown(
                    f"<div class=\"results-grid\">{''.join(cards)}</div>",
                    unsafe_allow_html=True,
                )

                wide_cards = [
                    render_result_card("Draft", result["draft"]),
                    render_result_card("Validation", result["validation"]),
                ]
                st.markdown(
                    f"<div class=\"results-wide\">{''.join(wide_cards)}</div>",
                    unsafe_allow_html=True,
                )
