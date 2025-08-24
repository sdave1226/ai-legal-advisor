import streamlit as st
import datetime
from typing import Dict, Optional
from dataclasses import dataclass
import openai
import os

# Load API key from Streamlit secrets
openai.api_key = st.secrets.get["OPENAI_API_KEY"]

if not openai.api_key:
    st.error("OpenAI API key is missing! Please set it in Streamlit Secrets.")

# Streamlit page config
st.set_page_config(
    page_title="AI Legal Advisor",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Categories
LEGAL_CATEGORIES = {
    "Contract Law": "Issues related to agreements and obligations",
    "Employment Law": "Workplace rights and employer obligations",
    "Property Law": "Real estate and property disputes",
    "Family Law": "Divorce, custody, and family matters",
    "Consumer Rights": "Purchases, warranties, and consumer protection",
    "Civil Law": "Personal injury, defamation, and civil disputes"
}

# Knowledge base fallback
FALLBACK_INFO = {
    "Contract Law": "Contracts require offer, acceptance, consideration, and mutual consent.",
    "Employment Law": "Employees have rights regarding wages, harassment, and safe work environments.",
    "Property Law": "Property disputes often relate to ownership, boundaries, or landlord-tenant laws.",
    "Family Law": "Family law governs divorce, custody, and adoption processes.",
    "Consumer Rights": "Consumers are protected against fraud and have warranty rights.",
    "Civil Law": "Civil law covers negligence, defamation, and personal injury cases."
}

@dataclass
class LegalQuery:
    question: str
    category: str
    timestamp: datetime.datetime
    response: Optional[str] = None

# Function to get GPT response
def get_gpt_response(question: str, category: str) -> str:
    if not openai.api_key:
        return f"⚠️ GPT not available. Here's some general info:\n\n{FALLBACK_INFO.get(category, '')}"

    try:
        prompt = f"""You are an AI Legal Advisor. Provide clear, concise, and general legal information (not legal advice).
Question: {question}
Category: {category}
Answer in simple language, and include a short disclaimer at the end."""

        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",  # lightweight and cost-efficient
            messages=[
                {"role": "system", "content": "You are a helpful legal information assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            temperature=0.5
        )

        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"⚠️ Error fetching GPT response. Using fallback:\n\n{FALLBACK_INFO.get(category, '')}"

# Navigation state
if "current_page" not in st.session_state:
    st.session_state.current_page = "Home"
if "queries" not in st.session_state:
    st.session_state.queries = []

# Sidebar
with st.sidebar:
    st.header("Navigation")
    if st.button("🏠 Home"): st.session_state.current_page = "Home"
    if st.button("ℹ️ About"): st.session_state.current_page = "About"
    if st.button("📋 Legal Cases"): st.session_state.current_page = "Legal Cases"

    st.markdown("---")
    st.header("Legal Topics")
    selected_category = st.selectbox("Select a legal area:", list(LEGAL_CATEGORIES.keys()))

    st.markdown("---")
    st.warning("This tool provides general info, not legal advice.")

# Main Content
st.markdown('<h1 style="text-align:center;">⚖️ AI Legal Advisor</h1>', unsafe_allow_html=True)

if st.session_state.current_page == "Home":
    st.header("Ask Your Legal Question")
    question = st.text_area("Enter your question:", height=150)
    if st.button("Get Legal Info", type="primary"):
        if question.strip():
            with st.spinner("Analyzing your question with AI..."):
                response = get_gpt_response(question, selected_category)
                st.markdown(f"### ✅ Answer\n{response}")
                st.session_state.queries.append(LegalQuery(question, selected_category, datetime.datetime.now(), response))
        else:
            st.warning("Please enter a question.")

elif st.session_state.current_page == "About":
    st.header("About AI Legal Advisor")
    st.write("""
    This AI-powered tool provides general legal information using GPT and a basic knowledge base.
    **Disclaimer:** This is for educational purposes only and does not replace professional legal advice.
    """)

elif st.session_state.current_page == "Legal Cases":
    st.header("Sample Legal Cases")
    st.info("Educational examples only.")
    for cat, desc in LEGAL_CATEGORIES.items():
        st.markdown(f"**{cat}**: {desc}")

# Query History
st.subheader("Your Previous Queries")
if st.session_state.queries:
    for q in st.session_state.queries:
        st.write(f"**{q.timestamp.strftime('%Y-%m-%d %H:%M')}** | {q.category}")
        st.write(f"Q: {q.question}")
        st.write(f"A: {q.response}")
        st.markdown("---")
else:
    st.info("No queries yet.")

# Footer
st.markdown("---")
st.caption("AI Legal Advisor v3.0 | Powered by Gauri | Educational Use Only")