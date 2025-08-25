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
        {"question": "What is a valid contract?", "answer": "A valid contract requires an offer, acceptance, consideration, and mutual consent. It must also comply with legal requirements and not involve illegal activity."},
        {"question": "What happens if a contract is breached?", "answer": "The non-breaching party can seek remedies such as monetary damages, specific performance, or termination of the agreement."},
        {"question": "Can a verbal agreement be legally binding?", "answer": "Yes, verbal agreements can be enforceable unless the law requires written contracts, such as for real estate or high-value transactions."},
        {"question": "What is a force majeure clause?", "answer": "A force majeure clause excuses parties from liability when an unforeseeable event beyond their control prevents them from fulfilling obligations."},
        {"question": "Can I cancel a contract after signing?", "answer": "It depends on the contract terms and local laws. Some contracts have cooling-off periods for cancellation."},
        {"question": "What is specific performance in contract law?", "answer": "Specific performance is a court order requiring a party to fulfill their contractual obligations rather than paying damages."},
        {"question": "Can contracts be modified after signing?", "answer": "Yes, but modifications must be agreed upon by all parties and usually documented in writing."},
        {"question": "What makes a contract void?", "answer": "A contract is void if it involves illegal activities, lacks essential terms, or parties lack legal capacity."},
        {"question": "What is the difference between void and voidable contracts?", "answer": "Void contracts have no legal effect, while voidable contracts are valid unless a party chooses to cancel them."},
        {"question": "What is an implied contract?", "answer": "An implied contract is formed through conduct or circumstances rather than written or spoken words."},
        {"question": "Can minors enter into a contract?", "answer": "Generally, contracts with minors are voidable, except for necessities like food and shelter."},
        {"question": "What is consideration in a contract?", "answer": "Consideration refers to something of value exchanged between parties, such as money or services."},
        {"question": "Can an email be considered a contract?", "answer": "Yes, if it shows mutual agreement and contains essential terms, emails can form a binding contract."},
        {"question": "What is anticipatory breach?", "answer": "Anticipatory breach occurs when a party indicates they will not perform their contractual obligations before the due date."},
        {"question": "Are non-compete clauses enforceable?", "answer": "It depends on jurisdiction and whether the clause is reasonable in scope and duration."},
        {"question": "Can a contract be terminated by mutual consent?", "answer": "Yes, both parties can agree to terminate a contract through a mutual agreement."},
        {"question": "What is a standard form contract?", "answer": "It’s a pre-drafted agreement where one party sets the terms, often used in consumer transactions."},
        {"question": "What are liquidated damages?", "answer": "Pre-agreed compensation specified in a contract if a party fails to meet obligations."},
        {"question": "What is a unilateral contract?", "answer": "A unilateral contract involves one party promising something in exchange for the other party’s performance."},
        {"question": "What is novation in contracts?", "answer": "Novation is replacing one party or obligation with another, creating a new contract with consent."}
    ],
    "Employment Law": [
        {"question": "Can an employer fire an employee without notice?", "answer": "In at-will employment states, yes, unless termination violates discrimination or retaliation laws."},
        {"question": "What are employee rights during termination?", "answer": "Employees are entitled to final pay, and in some jurisdictions, severance pay and notice periods."},
        {"question": "What is wrongful termination?", "answer": "Firing an employee for illegal reasons, such as discrimination or retaliation, constitutes wrongful termination."},
        {"question": "Can an employer reduce my salary without consent?", "answer": "No, salary changes usually require employee consent unless allowed under the contract."},
        {"question": "What is constructive dismissal?", "answer": "When working conditions are made intolerable, forcing the employee to resign."},
        {"question": "Do employees have the right to breaks?", "answer": "Yes, most labor laws require rest and meal breaks, though rules vary by jurisdiction."},
        {"question": "Can employers monitor employee emails?", "answer": "Yes, if the emails are sent through company systems and employees are informed."},
        {"question": "Is overtime pay mandatory?", "answer": "Yes, for eligible employees under labor laws, usually at 1.5 times the regular rate."},
        {"question": "What is employment discrimination?", "answer": "Unequal treatment based on race, gender, religion, age, or disability is prohibited."},
        {"question": "Are non-compete agreements enforceable?", "answer": "Enforceability depends on jurisdiction and reasonableness of scope and duration."},
        {"question": "What is sexual harassment at work?", "answer": "Unwelcome sexual advances, comments, or behavior creating a hostile work environment."},
        {"question": "Can employees refuse unsafe work?", "answer": "Yes, workers have the right to refuse unsafe conditions under occupational safety laws."},
        {"question": "Is an employment contract required by law?", "answer": "Many places allow verbal agreements, but written contracts are recommended."},
        {"question": "Can employers deduct wages for damages?", "answer": "Generally no, unless agreed upon or allowed by law."},
        {"question": "What is family leave?", "answer": "Time off for family or medical reasons, protected under laws like FMLA in the U.S."},
        {"question": "Can an employer change job duties?", "answer": "Yes, within reasonable limits and the employment agreement."},
        {"question": "Are interns entitled to pay?", "answer": "It depends on whether the internship meets specific educational criteria."},
        {"question": "Can an employee sue for unpaid wages?", "answer": "Yes, employees can file claims for unpaid wages or overtime."},
        {"question": "What are whistleblower protections?", "answer": "Laws protect employees who report illegal activities from retaliation."},
        {"question": "What is probationary employment?", "answer": "A trial period allowing employers to assess new hires before permanent employment."}
    ],
    "Property Law": [
        {"question": "What is property law?", "answer": "Property law governs ownership, use, and transfer of real estate and personal property."},
        {"question": "What is a property deed?", "answer": "A legal document that transfers property ownership from one person to another."},
        {"question": "Can property be jointly owned?", "answer": "Yes, joint ownership allows two or more people to share property rights."},
        {"question": "What is a mortgage?", "answer": "A loan secured by real property, where the lender can take the property if the borrower defaults."},
        {"question": "What is adverse possession?", "answer": "Acquiring ownership of property by occupying it openly for a certain time without the owner’s permission."},
        {"question": "What are property taxes?", "answer": "Taxes levied by local governments based on property value."},
        {"question": "Can a landlord evict a tenant without notice?", "answer": "No, legal notice is generally required before eviction."},
        {"question": "What is an easement?", "answer": "The right to use someone else’s property for a specific purpose, like a driveway or utility access."},
        {"question": "What is zoning law?", "answer": "Laws regulating how property can be used in specific areas (residential, commercial, etc.)."},
        {"question": "Can I sell property without clear title?", "answer": "No, clear title is needed to ensure legal ownership transfer."},
        {"question": "What is a property lien?", "answer": "A legal claim on property as security for a debt."},
        {"question": "Can tenants make changes to rented property?", "answer": "Only with landlord consent, unless the lease says otherwise."},
        {"question": "What is a lease agreement?", "answer": "A contract between landlord and tenant detailing rental terms."},
        {"question": "Who pays for property repairs in a rental?", "answer": "Usually landlords handle major repairs; tenants handle minor ones."},
        {"question": "What is eminent domain?", "answer": "The government’s right to take private property for public use with compensation."},
        {"question": "Can a property owner refuse to sell to someone?", "answer": "Yes, except for reasons that violate discrimination laws."},
        {"question": "What happens if property boundaries are unclear?", "answer": "A survey or court order may be needed to resolve disputes."},
        {"question": "What is squatting?", "answer": "Occupying a property without permission; may lead to adverse possession over time."},
        {"question": "Can property be inherited without a will?", "answer": "Yes, under laws of intestate succession."},
        {"question": "What is a title search?", "answer": "A check of property records to confirm legal ownership and find any liens."}
    ],
    "Family Law": [
        {"question": "What is family law?", "answer": "Family law governs issues like marriage, divorce, child custody, and adoption."},
        {"question": "How do I file for divorce?", "answer": "File a petition in family court, meet residency requirements, and serve your spouse."},
        {"question": "What is child custody?", "answer": "Legal responsibility for a child’s care, divided as sole or joint custody."},
        {"question": "Can grandparents seek visitation rights?", "answer": "Yes, in many jurisdictions if it’s in the child’s best interest."},
        {"question": "What is alimony?", "answer": "Financial support paid to a spouse after divorce."},
        {"question": "What is legal separation?", "answer": "A court-approved arrangement where spouses live apart but remain married."},
        {"question": "What is adoption?", "answer": "Legal process transferring parental rights from birth parents to adoptive parents."},
        {"question": "How is child support calculated?", "answer": "Based on parents’ income, number of children, and living expenses."},
        {"question": "Can child support orders be changed?", "answer": "Yes, if financial circumstances or child needs change."},
        {"question": "Is domestic violence a family law issue?", "answer": "Yes, courts issue protective orders to prevent abuse."},
        {"question": "Can same-sex couples adopt children?", "answer": "Yes, in many jurisdictions, subject to local laws."},
        {"question": "What is prenuptial agreement?", "answer": "A contract made before marriage defining property rights in case of divorce."},
        {"question": "Can paternity be disputed?", "answer": "Yes, through genetic testing and legal proceedings."},
        {"question": "Can a parent move out of state with a child?", "answer": "Usually requires court approval if custody orders exist."},
        {"question": "What is annulment?", "answer": "Legal declaration that a marriage never existed due to invalidity."},
        {"question": "Can minors marry?", "answer": "Only with parental consent and sometimes court approval."},
        {"question": "What is guardianship?", "answer": "Legal responsibility for another person, often a minor or disabled adult."},
        {"question": "Can custody be shared 50/50?", "answer": "Yes, if it’s in the child’s best interest and practical."},
        {"question": "How is property divided in divorce?", "answer": "Based on community property or equitable distribution rules."},
        {"question": "What is foster care?", "answer": "Temporary placement of children with approved caregivers when parents can’t provide care."}
    ],
    "Consumer Rights": [
        {"question": "What are consumer rights?", "answer": "Rights include safety, information, choice, and the right to be heard."},
        {"question": "Can I return a defective product?", "answer": "Yes, consumers have the right to repair, replacement, or refund for faulty products."},
        {"question": "What is a warranty?", "answer": "A guarantee by a seller that a product will perform as promised for a set time."},
        {"question": "Can businesses refuse refunds?", "answer": "Not for defective goods, but they can for buyer’s remorse unless stated."},
        {"question": "What is product liability?", "answer": "Legal responsibility of manufacturers for defective products causing harm."},
        {"question": "What is consumer fraud?", "answer": "Deceptive practices that mislead consumers into unfair transactions."},
        {"question": "Are online purchases protected?", "answer": "Yes, most consumer protection laws apply to e-commerce."},
        {"question": "Can I cancel an online order?", "answer": "Yes, before shipping or within a cooling-off period where applicable."},
        {"question": "What is false advertising?", "answer": "Misleading claims about a product or service."},
        {"question": "Can I sue a company for a defective product?", "answer": "Yes, under product liability laws."},
        {"question": "What is the cooling-off period?", "answer": "A time frame allowing consumers to cancel certain contracts without penalty."},
        {"question": "Are second-hand goods covered by consumer law?", "answer": "Yes, but warranties may differ from new goods."},
        {"question": "What are pyramid schemes?", "answer": "Fraudulent investment structures promising profits for recruiting others."},
        {"question": "Can I dispute a credit card charge?", "answer": "Yes, if unauthorized or for faulty goods/services."},
        {"question": "Are food products covered by consumer rights?", "answer": "Yes, they must meet safety and labeling standards."},
        {"question": "What is data protection for consumers?", "answer": "Laws safeguarding personal information from misuse."},
        {"question": "Can I return digital products?", "answer": "Depends on local laws and vendor policy."},
        {"question": "What is bait-and-switch advertising?", "answer": "Luring customers with low prices, then pushing higher-priced items."},
        {"question": "Can I claim compensation for delayed flights?", "answer": "Yes, under air passenger rights laws."},
        {"question": "What is a class action lawsuit?", "answer": "A lawsuit filed by a group of consumers with similar claims."}
    ],
    "Civil Law": [
        {"question": "What is civil law?", "answer": "Civil law deals with disputes between individuals or organizations, usually over rights and obligations."},
        {"question": "What is a tort?", "answer": "A wrongful act causing harm to another, leading to civil liability."},
        {"question": "What is negligence?", "answer": "Failure to exercise reasonable care, causing harm to others."},
        {"question": "Can I sue for emotional distress?", "answer": "Yes, if caused by another’s intentional or negligent act."},
        {"question": "What is defamation?", "answer": "Publishing false statements that harm someone’s reputation."},
        {"question": "What is the statute of limitations?", "answer": "Time limit for filing a lawsuit after an event occurs."},
        {"question": "Can I sue for breach of privacy?", "answer": "Yes, if someone unlawfully intrudes on your personal life."},
        {"question": "What is strict liability?", "answer": "Liability without proof of negligence, often in product defect cases."},
        {"question": "Can minors be sued?", "answer": "Yes, but liability may be limited or transferred to parents."},
        {"question": "What is a civil judgment?", "answer": "A court’s final decision in a civil case."},
        {"question": "Can civil cases involve jail time?", "answer": "No, civil cases result in fines or compensation, not imprisonment."},
        {"question": "What is small claims court?", "answer": "A court for resolving low-value disputes without expensive litigation."},
        {"question": "What is comparative negligence?", "answer": "When both parties share fault, damages are reduced based on contribution."},
        {"question": "Can I appeal a civil case?", "answer": "Yes, within the time limit and based on legal grounds."},
        {"question": "What is injunction relief?", "answer": "A court order requiring a person to do or stop doing something."},
        {"question": "Can landlords be sued for unsafe housing?", "answer": "Yes, if they fail to maintain habitable conditions."},
        {"question": "What is a class action in civil law?", "answer": "A lawsuit filed by a group of plaintiffs against a defendant."},
        {"question": "Can I settle a civil case out of court?", "answer": "Yes, through negotiation or mediation."},
        {"question": "What are compensatory damages?", "answer": "Money awarded to compensate for actual losses."},
        {"question": "What are punitive damages?", "answer": "Additional damages to punish wrongful conduct and deter others."}
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
    faq_questions = [item["question"] for item in faqs]
    
    # Find best match using rapidfuzz
    best_match, score, idx = process.extractOne(question, faq_questions, scorer=fuzz.token_sort_ratio)
    
    if score > 60:  # Acceptable threshold
        return faqs[idx]["answer"]
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
        # Question + Category + Timestamp (timestamp at end, small font)
        st.markdown(
            f"**Q:** {q.question}  |  *{q.category}* "
            f"<span style='font-size: 12px; color: gray;'>({q.timestamp.strftime('%Y-%m-%d %H:%M')})</span>",
            unsafe_allow_html=True
        )
        # Answer
        st.write(f"**A:** {q.response}")
        st.markdown("---")
else:
    st.info("No queries yet.")

# ------------------------------
# Footer
# ------------------------------
st.markdown("---")
st.caption("AI Legal Advisor v3.0 | Powered by Gaurishankar Kewat | Educational Use Only")