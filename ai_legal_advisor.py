import streamlit as st
import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass

# Set page configuration
st.set_page_config(
    page_title="AI Legal Advisor",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        color: #1e3a8a;
        text-align: center;
        margin-bottom: 2rem;
    }
    .disclaimer {
        background-color: #fef3c7;
        border-left: 4px solid #f59e0b;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 4px;
    }
    
    .legal-card {
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 1.5rem;
        margin: 1rem 0;
    }
    .case-card {
        background-color: #e8f4f8;
        border-left: 4px solid #0288d1;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 4px;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state for navigation
if 'current_page' not in st.session_state:
    st.session_state.current_page = "Home"

# Legal knowledge base
LEGAL_CATEGORIES = {
    "Contract Law": "Issues related to agreements and obligations",
    "Employment Law": "Workplace rights and employer obligations",
    "Property Law": "Real estate and property disputes",
    "Family Law": "Divorce, custody, and family matters",
    "Consumer Rights": "Purchases, warranties, and consumer protection",
    "Civil Law": "Personal injury, defamation, and civil disputes"
}

# Sample legal cases
LEGAL_CASES = [
    {
        "title": "Smith v. Johnson Contract Dispute",
        "category": "Contract Law",
        "summary": "Dispute over breach of service agreement for home renovation",
        "outcome": "Settlement reached with compensation for incomplete work",
        "key_points": ["Written contracts are essential", "Document all communications", "Consider mediation before litigation"]
    },
    {
        "title": "Doe v. TechCorp Employment Case",
        "category": "Employment Law",
        "summary": "Wrongful termination claim based on discrimination",
        "outcome": "Jury awarded damages for emotional distress and lost wages",
        "key_points": ["Keep records of performance reviews", "Understand your rights", "Report discrimination promptly"]
    },
    {
        "title": "Brown v. Green Property Dispute",
        "category": "Property Law",
        "summary": "Boundary dispute between neighboring properties",
        "outcome": "Court ordered survey and boundary adjustment",
        "key_points": ["Get professional surveys", "Check property deeds", "Mediation can save costs"]
    },
    {
        "title": "Williams Family Custody Case",
        "category": "Family Law",
        "summary": "Child custody modification after relocation",
        "outcome": "Joint custody maintained with adjusted visitation schedule",
        "key_points": ["Best interests of child paramount", "Consider mediation", "Document all interactions"]
    }
]

# Navigation function
def navigate_to(page):
    st.session_state.current_page = page

# Header
st.markdown('<h1 class="main-header">AI Legal Advisor</h1>', unsafe_allow_html=True)

# Disclaimer
st.warning("""
    ⚠️ Important Disclaimer: This AI Legal Advisor is for educational and informational purposes only. 
        It does not constitute legal advice. Always consult with a qualified attorney for specific legal matters.
""")

# Sidebar navigation
with st.sidebar:
    st.header("Navigation")
    
    if st.button("🏠 Home", key="home_btn"):
        navigate_to("Home")
    
    if st.button("ℹ️ About", key="about_btn"):
        navigate_to("About")
    
    if st.button("📋 Legal Cases", key="cases_btn"):
        navigate_to("Legal Cases")
    
    st.markdown("---")
    
    st.header("Legal Topics")
    selected_category = st.selectbox(
        "Select a legal area:",
        list(LEGAL_CATEGORIES.keys())
    )
    
    st.markdown("---")
    
    st.header("⚠️ Important")
    st.warning(
        "This AI Legal Advisor provides general information only and is not a substitute for professional legal advice. "
        "For complex legal matters, please consult with a qualified attorney."
    )

# Main content based on current page
if st.session_state.current_page == "Home":
    st.header("Welcome to AI Legal Advisor")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Ask Your Legal Question")
        
        question = st.text_area(
            "Describe your legal situation or question:",
            placeholder="Example: I signed a contract but the other party didn't fulfill their obligations...",
            height=150
        )
        
        context = st.text_area(
            "Provide additional context (optional):",
            placeholder="Any relevant dates, parties involved, jurisdiction, etc.",
            height=100
        )
        
        if st.button("Get Legal Information", type="primary", use_container_width=True):
            if question:
                with st.spinner("Analyzing your question..."):
                    st.markdown("""
                        <div class="legal-card">
                            <h3>Analysis Result</h3>
                            <p><strong>Based on your question about:</strong> {}</p>
                            <p><strong>General Information:</strong></p>
                            <ul>
                                <li>This appears to relate to {} law</li>
                                <li>Key considerations typically include...</li>
                                <li>Common legal principles that may apply...</li>
                            </ul>
                            <p><strong>Important:</strong> This is general information only. 
                            Consult a qualified attorney for advice specific to your situation.</p>
                        </div>
                    """.format(question[:50] + "...", selected_category), unsafe_allow_html=True)
            else:
                st.warning("Please enter a legal question to get started.")
    
    with col2:
        st.subheader("Quick Resources")
        
        with st.expander("Legal Terms Glossary"):
            st.write("""
            - **Breach of Contract**: Failure to fulfill contractual obligations
            - **Liability**: Legal responsibility for damages
            - **Jurisdiction**: Authority of a court to hear a case
            - **Statute of Limitations**: Time limit for filing a lawsuit
            """)
        
        with st.expander("When to Consult a Lawyer"):
            st.write("""
            - Complex legal situations
            - Court proceedings involved
            - High financial stakes
            - Criminal matters
            - Real estate transactions
            """)

elif st.session_state.current_page == "About":
    st.header("About AI Legal Advisor")
    
    st.markdown("""
    ### What is AI Legal Advisor?
    
    AI Legal Advisor is an educational tool designed to provide general legal information and guidance. 
    It helps users understand basic legal concepts and common legal situations.
    
    ### Features
    
    - **Legal Q&A**: Ask questions about various legal topics
    - **Legal Cases**: Browse sample cases and outcomes
    - **Educational Resources**: Learn about different areas of law
    - **Document Guidance**: Understand what legal documents you might need
    
    ### How to Use
    
    1. **Navigate** using the sidebar buttons
    2. **Select** a legal area that matches your question
    3. **Ask** your question in the text area
    4. **Review** the general information provided
    5. **Consult** a qualified attorney for specific advice
    
    ### Limitations
    
    - **Not Legal Advice**: This tool provides general information only
    - **Educational Purpose**: Designed for learning and awareness
    - **Jurisdiction Variations**: Laws vary by location
    - **Complex Cases**: Complex situations require professional consultation
    
    ### When to Seek Professional Help
    
    - **Criminal charges** or investigations
    - **Lawsuits** or court proceedings
    - **High-value transactions**
    - **Family law matters** (divorce, custody)
    - **Business formation** or contracts
    - **Real estate transactions**
    """)

elif st.session_state.current_page == "Legal Cases":
    st.header("Legal Cases Database")
    
    st.markdown("### Browse Sample Legal Cases")
    st.info("These are sample cases for educational purposes. Real cases may have different outcomes.")
    
    # Filter by category
    filter_category = st.selectbox("Filter by category:", ["All"] + list(LEGAL_CATEGORIES.keys()))
    
    # Display cases
    st.markdown("""
        <style>
        .case-card {
            color: black !important;   /* force black text */
            background-color: #f5f5f5; /* optional: light grey bg so black is visible in dark theme */
            padding: 10px;
            border-radius: 6px;
        }
        </style>
    """, unsafe_allow_html=True)

    for case in LEGAL_CASES:
        if filter_category == "All" or case["category"] == filter_category:
            with st.expander(f"**{case['title']}** - {case['category']}"):
                st.markdown(f"""
                <div class="case-card" font-color="#black">
                <strong>Summary:</strong> {case['summary']}<br>
                <strong>Outcome:</strong> {case['outcome']}<br>
                <strong>Key Learning Points:</strong>
                </div>
                """, unsafe_allow_html=True)
                
                for point in case["key_points"]:
                    st.write(f"• {point}")

# Footer
st.markdown("---")
st.markdown("""
    AI Legal Advisor v2.0 | Educational Legal Information System
    © 2025 - For Educational Purposes Only | Not a substitute for professional legal advice
""")
