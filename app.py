# import streamlit as st
# import datetime
# from typing import Optional
# from dataclasses import dataclass
# import requests
# import os

# # Streamlit page config
# st.set_page_config(
#     page_title="AI Legal Advisor",
#     page_icon="⚖️",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# # Hugging Face API settings
# HUGGINGFACE_API_KEY = st.secrets.get("HUGGINGFACE_API_KEY") or os.getenv("HUGGINGFACE_API_KEY")
# # After setting HUGGINGFACE_API_KEY
# API_URL = "https://api-inference.huggingface.co/models/distilgpt2"

# headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}

# # Categories
# LEGAL_CATEGORIES = {
#     "Contract Law": "Issues related to agreements and obligations",
#     "Employment Law": "Workplace rights and employer obligations",
#     "Property Law": "Real estate and property disputes",
#     "Family Law": "Divorce, custody, and family matters",
#     "Consumer Rights": "Purchases, warranties, and consumer protection",
#     "Civil Law": "Personal injury, defamation, and civil disputes"
# }

# # Knowledge base fallback
# FALLBACK_INFO = {
#     "Contract Law": "Contracts require offer, acceptance, consideration, and mutual consent.",
#     "Employment Law": "Employees have rights regarding wages, harassment, and safe work environments.",
#     "Property Law": "Property disputes often relate to ownership, boundaries, or landlord-tenant laws.",
#     "Family Law": "Family law governs divorce, custody, and adoption processes.",
#     "Consumer Rights": "Consumers are protected against fraud and have warranty rights.",
#     "Civil Law": "Civil law covers negligence, defamation, and personal injury cases."
# }

# @dataclass
# class LegalQuery:
#     question: str
#     category: str
#     timestamp: datetime.datetime
#     response: Optional[str] = None

# # Hugging Face API call
# # def get_ai_response(question: str, category: str) -> str:
# #     if not HUGGINGFACE_API_KEY:
# #         return f"⚠️ Hugging Face API key missing. Add it in Streamlit Secrets."
    
# #     prompt = f"""You are an AI Legal Advisor. Provide general legal information (not legal advice).
# # Question: {question}
# # Category: {category}
# # Answer in clear, simple language and include a short disclaimer at the end."""
    
# #     try:
# #         response = requests.post(API_URL, headers=headers, json={"inputs": prompt})
# #         if response.status_code == 200:
# #             result = response.json()
# #             if isinstance(result, list) and "generated_text" in result[0]:
# #                 return result[0]["generated_text"]
# #             else:
# #                 return "⚠️ Unexpected response format from Hugging Face API."
# #         else:
# #             return f"⚠️ API Error: {response.status_code}, {response.text}"
# #     except Exception as e:
# #         return f"⚠️ Error contacting Hugging Face API: {str(e)}"

# def get_ai_response(question: str, category: str) -> str:
#     if not HUGGINGFACE_API_KEY:
#         return f"⚠️ Hugging Face API key missing. Add it in Streamlit Secrets."

#     prompt = f"""You are an AI Legal Advisor. Provide general legal information (not legal advice).
# Question: {question}
# Category: {category}
# Answer in clear, simple language and include a short disclaimer at the end."""

#     try:
#         st.write(f"🔍 Debug: Sending prompt to Hugging Face: {prompt}")
#         response = requests.post(API_URL, headers=headers, json={"inputs": prompt})
#         st.write(f"🔍 Debug: API Response Status Code: {response.status_code}")
#         st.write(f"🔍 Debug: Raw API Response: {response.text}")

#         if response.status_code == 200:
#             result = response.json()
#             if isinstance(result, list) and "generated_text" in result[0]:
#                 return result[0]["generated_text"]
#             else:
#                 return "⚠️ Unexpected response format from Hugging Face API."
#         else:
#             return f"⚠️ API Error: {response.status_code}, {response.text}"
#     except Exception as e:
#         return f"⚠️ Error contacting Hugging Face API: {str(e)}"

# # Navigation state
# if "current_page" not in st.session_state:
#     st.session_state.current_page = "Home"
# if "queries" not in st.session_state:
#     st.session_state.queries = []

# # Sidebar
# with st.sidebar:
#     st.header("Navigation")
#     if st.button("🏠 Home"): st.session_state.current_page = "Home"
#     if st.button("ℹ️ About"): st.session_state.current_page = "About"
#     if st.button("📋 Legal Cases"): st.session_state.current_page = "Legal Cases"

#     st.markdown("---")
#     st.header("Legal Topics")
#     selected_category = st.selectbox("Select a legal area:", list(LEGAL_CATEGORIES.keys()))

#     st.markdown("---")
#     st.warning("This tool provides general info, not legal advice.")

# # Main Content
# st.markdown('<h1 style="text-align:center;">⚖️ AI Legal Advisor</h1>', unsafe_allow_html=True)

# if st.session_state.current_page == "Home":
#     st.header("Ask Your Legal Question")
#     question = st.text_area("Enter your question:", height=150)
#     if st.button("Get Legal Info", type="primary"):
#         if question.strip():
#             with st.spinner("Analyzing your question using AI..."):
#                 response = get_ai_response(question, selected_category)
#                 st.markdown(f"### ✅ Answer\n{response}")
#                 st.session_state.queries.append(LegalQuery(question, selected_category, datetime.datetime.now(), response))
#         else:
#             st.warning("Please enter a question.")

# elif st.session_state.current_page == "About":
#     st.header("About AI Legal Advisor")
#     st.write("""
#     This AI-powered tool provides general legal information using free Hugging Face models and a basic knowledge base.
#     **Disclaimer:** This is for educational purposes only and does not replace professional legal advice.
#     """)

# elif st.session_state.current_page == "Legal Cases":
#     st.header("Sample Legal Cases")
#     st.info("Educational examples only.")
#     for cat, desc in LEGAL_CATEGORIES.items():
#         st.markdown(f"**{cat}**: {desc}")

# # Query History
# st.subheader("Your Previous Queries")
# if st.session_state.queries:
#     for q in st.session_state.queries:
#         st.write(f"**{q.timestamp.strftime('%Y-%m-%d %H:%M')}** | {q.category}")
#         st.write(f"Q: {q.question}")
#         st.write(f"A: {q.response}")
#         st.markdown("---")
# else:
#     st.info("No queries yet.")

# # Footer
# st.markdown("---")
# st.caption("AI Legal Advisor v3.0 | Powered by Gaurishankar Kewat | Educational Use Only")

import streamlit as st
import datetime
from typing import Optional
from dataclasses import dataclass
from rapidfuzz import process, fuzz

# ------------------------------
# Streamlit page config
# ------------------------------
st.set_page_config(
    page_title="AI Legal Advisor",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ------------------------------
# Categories
# ------------------------------
LEGAL_CATEGORIES = {
    "Contract Law": "Issues related to agreements and obligations",
    "Employment Law": "Workplace rights and employer obligations",
    "Property Law": "Real estate and property disputes",
    "Family Law": "Divorce, custody, and family matters",
    "Consumer Rights": "Purchases, warranties, and consumer protection",
    "Civil Law": "Personal injury, defamation, and civil disputes"
}

# ------------------------------
# Knowledge Base (600 FAQs)
# ------------------------------
LEGAL_FAQS = {
    "Contract Law": [
        {"q": "What is a contract?", "a": "A contract is a legally binding agreement between two or more parties."},
        {"q": "What are the essential elements of a contract?", "a": "Offer, acceptance, consideration, and mutual consent are required for a valid contract."},
        {"q": "What is consideration in contract law?", "a": "Consideration refers to something of value exchanged between parties in a contract."},
        {"q": "What happens if a contract is breached?", "a": "If a contract is breached, the non-breaching party may seek remedies like damages or specific performance."},
        # ... Add 96 more for Contract Law
    ],
    "Employment Law": [
        {"q": "What is employment law?", "a": "Employment law regulates the relationship between employers and employees."},
        {"q": "What rights do employees have regarding wages?", "a": "Employees are entitled to minimum wage and overtime pay as per labor laws."},
        {"q": "What is wrongful termination?", "a": "Wrongful termination occurs when an employee is fired in violation of the law or a contract."},
        # ... Add 97 more for Employment Law
    ],
    "Property Law": [
        {"q": "What is property law?", "a": "Property law governs ownership and use of land and buildings."},
        {"q": "What are property rights?", "a": "Property rights include the right to use, sell, and enjoy property legally owned."},
        {"q": "What is adverse possession?", "a": "Adverse possession allows someone to claim ownership of land if they occupy it for a specific period under certain conditions."},
        # ... Add 97 more for Property Law
    ],
    "Family Law": [
        {"q": "What is family law?", "a": "Family law deals with issues like marriage, divorce, and child custody."},
        {"q": "How is child custody decided?", "a": "Child custody is determined based on the best interest of the child."},
        {"q": "What is alimony?", "a": "Alimony is financial support paid to a spouse after separation or divorce."},
        # ... Add 97 more for Family Law
    ],
    "Consumer Rights": [
        {"q": "What are consumer rights?", "a": "Consumer rights protect buyers from unfair practices and ensure product safety."},
        {"q": "What is a warranty?", "a": "A warranty is a guarantee provided by a seller regarding product quality and durability."},
        {"q": "What can I do if a product is defective?", "a": "You can request a repair, replacement, or refund under consumer protection laws."},
        # ... Add 97 more for Consumer Rights
    ],
    "Civil Law": [
        {"q": "What is civil law?", "a": "Civil law deals with disputes between individuals or organizations, typically involving compensation."},
        {"q": "What is a tort?", "a": "A tort is a wrongful act or omission that causes harm to another person."},
        {"q": "What is defamation?", "a": "Defamation is the act of damaging someone's reputation by making false statements."},
        # ... Add 97 more for Civil Law
    ]
}

# ------------------------------
# Data Model for Query History
# ------------------------------
@dataclass
class LegalQuery:
    question: str
    category: str
    timestamp: datetime.datetime
    response: Optional[str] = None

# ------------------------------
# Fuzzy Search Logic
# ------------------------------
def find_best_answer(question: str, category: str) -> str:
    faqs = LEGAL_FAQS.get(category, [])
    if not faqs:
        return "No data available for this category."
    
    # Extract questions
    faq_questions = [item["q"] for item in faqs]
    
    # Find best match using rapidfuzz
    best_match, score, idx = process.extractOne(question, faq_questions, scorer=fuzz.token_sort_ratio)
    
    if score > 60:  # Acceptable threshold
        return faqs[idx]["a"]
    else:
        return "Sorry, no close match found. Please try rephrasing your question."

# ------------------------------
# Navigation state
# ------------------------------
if "current_page" not in st.session_state:
    st.session_state.current_page = "Home"
if "queries" not in st.session_state:
    st.session_state.queries = []

# ------------------------------
# Sidebar Navigation
# ------------------------------
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

# ------------------------------
# Main Content
# ------------------------------
st.markdown('<h1 style="text-align:center;">⚖️ AI Legal Advisor</h1>', unsafe_allow_html=True)

if st.session_state.current_page == "Home":
    st.header("Ask Your Legal Question")
    question = st.text_area("Enter your question:", height=150)
    if st.button("Get Legal Info", type="primary"):
        if question.strip():
            with st.spinner("Searching for the best answer..."):
                response = find_best_answer(question, selected_category)
                st.markdown(f"### ✅ Answer\n{response}")
                st.session_state.queries.append(LegalQuery(question, selected_category, datetime.datetime.now(), response))
        else:
            st.warning("Please enter a question.")

elif st.session_state.current_page == "About":
    st.header("About AI Legal Advisor")
    st.write("""
    This AI-powered tool provides general legal information using an offline knowledge base of FAQs.
    **Disclaimer:** This is for educational purposes only and does not replace professional legal advice.
    """)

elif st.session_state.current_page == "Legal Cases":
    st.header("Sample Legal Cases")
    st.info("Educational examples only.")
    for cat, desc in LEGAL_CATEGORIES.items():
        st.markdown(f"**{cat}**: {desc}")

# ------------------------------
# Query History
# ------------------------------
st.subheader("Your Previous Queries")
if st.session_state.queries:
    for q in st.session_state.queries:
        st.write(f"**{q.timestamp.strftime('%Y-%m-%d %H:%M')}** | {q.category}")
        st.write(f"Q: {q.question}")
        st.write(f"A: {q.response}")
        st.markdown("---")
else:
    st.info("No queries yet.")

# ------------------------------
# Footer
# ------------------------------
st.markdown("---")
st.caption("AI Legal Advisor v3.0 | Powered by Gaurishankar Kewat | Educational Use Only")
