import streamlit as st
import anthropic
import os
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()

# Create Anthropic client — your connection to Claude API
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# ── Page config ───────────────────────────────────────────
st.set_page_config(
    page_title="IncidentLens AI",
    page_icon="🔍",
    layout="centered"
)

# ── System prompt — this is the brain of your app ─────────
# This tells Claude exactly how to behave.
# Good prompt engineering = good app output.
SYSTEM_PROMPT = """You are IncidentLens AI — an expert data engineering incident analyst.

You help data engineers diagnose pipeline failures, identify root causes, 
and generate professional documentation.

When a user describes an incident, structure your response in exactly these sections:

## 🔍 Root Cause Analysis
Identify the most likely root cause. Give a confidence level: High / Medium / Low.
Explain your reasoning in 2-3 sentences.

## 🛠️ Fix Steps
List fix steps in priority order. Number each step.
Be specific — include exact actions, commands, or checks where relevant.

## ⚠️ Prevention
2-3 concrete steps to prevent this happening again.

## 📋 Confluence Runbook Entry
Generate a ready-to-paste Confluence runbook entry in this exact format:

**Incident Title:** [descriptive title]
**Date Logged:** [leave blank for user to fill]
**Environment:** [from user input]
**Pipeline/System:** [from user input]

**Problem Statement:**
[Clear description of what broke and impact]

**Root Cause:**
[Root cause identified]

**Resolution Steps:**
1. [step]
2. [step]
3. [step]

**Prevention Measures:**
[Prevention steps]

**Related Issues:** [leave blank for user to fill]
**Resolved By:** [leave blank for user to fill]

---
After the first analysis, answer follow-up questions conversationally.
You are talking to an experienced data engineer — be specific and technical."""

# ── Session state — keeps conversation alive ──────────────
# Anthropic API has no memory — you must send full history
# every single call. Streamlit session_state stores it.
if "messages" not in st.session_state:
    st.session_state.messages = []
if "incident_analysed" not in st.session_state:
    st.session_state.incident_analysed = False

# ── Header ─────────────────────────────────────────────────
st.title("🔍 IncidentLens AI")
st.markdown("**Data Pipeline Incident Analyser** — diagnose failures and generate Confluence runbook entries instantly.")
st.divider()

# ── Input form ─────────────────────────────────────────────
st.markdown("#### Describe your incident")

col1, col2 = st.columns(2)
with col1:
    pipeline_name = st.text_input(
        "Pipeline / System name",
        placeholder="e.g. Daily Portfolio Optimisation"
    )
with col2:
    environment = st.selectbox(
        "Environment",
        ["Production", "UAT", "QA", "Development"]
    )

error_description = st.text_area(
    "What broke? Paste error log or describe the failure:",
    height=150,
    placeholder="e.g. Job failed at 10:47am. Error: ORA-01403 No data found in HOLDINGS_STAGING. SLA breach at 11am..."
)

already_tried = st.text_area(
    "What have you already tried?",
    height=80,
    placeholder="e.g. Restarted the job, checked vendor file arrived, verified ISIN codes..."
)

col1, col2 = st.columns([1, 4])
with col1:
    analyse_btn = st.button(
        "🔍 Analyse",
        type="primary",
        use_container_width=True
    )
with col2:
    if st.button("🔄 New incident", use_container_width=False):
        st.session_state.messages = []
        st.session_state.incident_analysed = False
        st.rerun()

# ── Display conversation history ───────────────────────────
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ── Analyse button logic ───────────────────────────────────
if analyse_btn and error_description.strip():

    # Build the user message from all inputs
    user_message = f"""
** {pipeline_name if pipeline_name else 'Not specified'}
**Environment:** {environment}

**Incident Description:**
{error_description}

**Already Tried:**
{already_tried if already_tried else 'Nothing yet'}
"""

    # Add to history and show in UI
    st.session_state.messages.append({
        "role": "user",
        "content": user_message
    })

    with st.chat_message("user"):
        st.markdown(user_message)

    # Call Claude API
    with st.chat_message("assistant"):
        with st.spinner("Analysing incident..."):
            response = client.messages.create(
                model="claude-haiku-4-5",
                max_tokens=2000,
                system=SYSTEM_PROMPT,
                messages=st.session_state.messages
            )
            reply = response.content[0].text
        st.markdown(reply)

    # Save reply to history
    st.session_state.messages.append({
        "role": "assistant",
        "content": reply
    })
    st.session_state.incident_analysed = True

elif analyse_btn and not error_description.strip():
    st.warning("Please describe the incident before analysing.")

# ── Follow-up chat ─────────────────────────────────────────
if st.session_state.incident_analysed:
    st.divider()
    st.markdown("**Ask a follow-up question:**")

    if follow_up := st.chat_input(
        "e.g. Can you explain step 2 in more detail? What if the vendor file is missing?"
    ):
        st.session_state.messages.append({
            "role": "user",
            "content": follow_up
        })

        with st.chat_message("user"):
            st.markdown(follow_up)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = client.messages.create(
                    model="claude-haiku-4-5",
                    max_tokens=1000,
                    system=SYSTEM_PROMPT,
                    messages=st.session_state.messages
                )
                reply = response.content[0].text
            st.markdown(reply)

        st.session_state.messages.append({
            "role": "assistant",
            "content": reply
        })