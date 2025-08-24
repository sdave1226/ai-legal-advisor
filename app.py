import streamlit as st
import datetime
from typing import Optional
from dataclasses import dataclass
import requests
import os

# Streamlit page config
st.set_page_config(
    page_title="AI Legal Advisor",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Hugging Face API settings
HUGGINGFACE_API_KEY = st.secrets.get("HUGGINGFACE_API_KEY") or os.getenv("HUGGINGFACE_API_KEY")
print(f"Hugging Face API Key: {HUGGINGFACE_API_KEY}")
API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-large"
headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}

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

# Hugging Face API call
def get_ai_response(question: str, category: str) -> str:
    if not HUGGINGFACE_API_KEY:
        return f"⚠️ Hugging Face API key missing. Add it in Streamlit Secrets."
    
    prompt = f"""You are an AI Legal Advisor. Provide general legal information (not legal advice).
Question: {question}
Category: {category}
Answer in clear, simple language and include a short disclaimer at the end."""
    
    try:
        response = requests.post(API_URL, headers=headers, json={"inputs": prompt})
        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and "generated_text" in result[0]:
                return result[0]["generated_text"]
            else:
                return "⚠️ Unexpected response format from Hugging Face API."
        else:
            return f"⚠️ API Error: {response.status_code}, {response.text}"
    except Exception as e:
        return f"⚠️ Error contacting Hugging Face API: {str(e)}"

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
            with st.spinner("Analyzing your question using AI..."):
                response = get_ai_response(question, selected_category)
                st.markdown(f"### ✅ Answer\n{response}")
                st.session_state.queries.append(LegalQuery(question, selected_category, datetime.datetime.now(), response))
        else:
            st.warning("Please enter a question.")

elif st.session_state.current_page == "About":
    st.header("About AI Legal Advisor")
    st.write("""
    This AI-powered tool provides general legal information using free Hugging Face models and a basic knowledge base.
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
st.caption("AI Legal Advisor v3.0 | Powered by Gaurishankar Kwat | Educational Use Only")
