import streamlit as st
import json
import datetime
from typing import Dict, List, Optional
import re
from dataclasses import dataclass
from enum import Enum

# Configure Streamlit page
st.set_page_config(
    page_title="AI Legal Advisor",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

class LegalCategory(Enum):
    CIVIL_LAW = "Civil Law"
    FAMILY_LAW = "Family Law"
    PROPERTY_LAW = "Property Law"
    CONSUMER_RIGHTS = "Consumer Rights"
    EMPLOYMENT_LAW = "Employment Law"
    CONTRACT_LAW = "Contract Law"

@dataclass
class LegalQuery:
    question: str
    category: LegalCategory
    timestamp: datetime.datetime
    response: Optional[str] = None

class LegalKnowledgeBase:
    def __init__(self):
        self.knowledge_base = {
            LegalCategory.CIVIL_LAW: {
                "defamation": "Defamation involves false statements that harm someone's reputation...",
                "negligence": "Negligence occurs when someone fails to exercise reasonable care...",
                "personal injury": "Personal injury claims arise when someone is harmed..."
            },
            LegalCategory.FAMILY_LAW: {
                "divorce": "Divorce procedures vary by jurisdiction...",
                "child custody": "Child custody decisions prioritize the best interests...",
                "adoption": "Adoption processes involve legal termination..."
            },
            LegalCategory.PROPERTY_LAW: {
                "landlord tenant": "Landlord-tenant law governs rental relationships...",
                "real estate": "Real estate transactions require proper documentation...",
                "property disputes": "Property disputes often involve boundary issues..."
            },
            LegalCategory.CONSUMER_RIGHTS: {
                "fraud": "Consumer fraud involves deceptive practices...",
                "warranty": "Warranty rights protect consumers...",
                "debt collection": "Debt collectors must follow fair practices..."
            },
            LegalCategory.EMPLOYMENT_LAW: {
                "wrongful termination": "Wrongful termination occurs when firing violates law...",
                "workplace harassment": "Workplace harassment based on protected characteristics...",
                "wage disputes": "Employees have rights to minimum wage..."
            },
            LegalCategory.CONTRACT_LAW: {
                "breach of contract": "Contract breach occurs when one party fails...",
                "contract formation": "Valid contracts require offer, acceptance...",
                "contract disputes": "Contract disputes often arise from ambiguous terms..."
            }
        }

    def search_knowledge(self, query: str, category: LegalCategory) -> str:
        """Search knowledge base for relevant information"""
        query_lower = query.lower()
        category_knowledge = self.knowledge_base.get(category, {})
        
        # Simple keyword matching
        for topic, info in category_knowledge.items():
            if any(keyword in query_lower for keyword in topic.split()):
                return f"**{topic.title()}**: {info}"
        
        return f"For {category.value} matters, I recommend consulting with a qualified attorney..."

class DocumentTemplates:
    @staticmethod
    def rental_agreement(landlord_name: str, tenant_name: str, property_address: str, 
                        monthly_rent: str, lease_term: str) -> str:
        return f"""
RENTAL AGREEMENT

This Rental Agreement is entered into on {datetime.date.today().strftime('%B %d, %Y')} between:
[Complete template content...]
"""

    @staticmethod
    def employment_contract(employer_name: str, employee_name: str, position: str, 
                          salary: str, start_date: str) -> str:
        return f"""
EMPLOYMENT AGREEMENT
[Complete template content...]
"""

    @staticmethod
    def service_agreement(service_provider: str, client_name: str, service_description: str, 
                         payment_amount: str, completion_date: str) -> str:
        return f"""
SERVICE AGREEMENT
[Complete template content...]
"""

def main():
    # Initialize session state
    if 'queries' not in st.session_state:
        st.session_state.queries = []
    if 'knowledge_base' not in st.session_state:
        st.session_state.knowledge_base = LegalKnowledgeBase()

    # Header
    st.title("⚖️ AI Legal Advisor")
    st.markdown("*Your intelligent assistant for basic legal guidance and document drafting*")
    
    # Sidebar
    with st.sidebar:
        st.header("📋 Navigation")
        page = st.selectbox(
            "Choose a service:",
            ["Legal Q&A", "Document Generator", "Legal Resources", "Query History"]
        )
        
        st.markdown("---")
        st.markdown("### ⚠️ Important Disclaimer")
        st.warning(
            "This AI Legal Advisor provides general information only and is not a substitute for professional legal advice. "
            "For complex legal matters, please consult with a qualified attorney."
        )
        
    if __name__ == "__main__":
        main()
