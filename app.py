import streamlit as st
import openai
from datetime import datetime
import os

# Hugging Face for fallback
from transformers import pipeline

# Load OpenAI API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

# Load Hugging Face fallback model (small for free usage)
hf_generator = pipeline("text-generation", model="distilgpt2")

# Streamlit app
st.set_page_config(page_title="AI Legal Advisor", layout="wide")

st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "About", "Legal Cases"])

# Session state to store queries
if "queries" not in st.session_state:
    st.session_state["queries"] = []

if page == "Home":
    st.title("⚖️ Ask Your Legal Question")

    user_question = st.text_area("Enter your question:")
    legal_area = st.selectbox("Select a legal area:", ["Contract Law", "Criminal Law", "Family Law", "Property Law", "Other"])

    if st.button("Get Legal Info"):
        answer = None
        try:
            # Try OpenAI first
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a legal information assistant. Provide general legal information, not advice."},
                    {"role": "user", "content": f"Legal area: {legal_area}. Question: {user_question}"}
                ],
                max_tokens=200
            )
            answer = response["choices"][0]["message"]["content"]

        except openai.error.RateLimitError as e:
            st.warning("⚠️ OpenAI quota exceeded. Using fallback model.")
            # Hugging Face fallback
            hf_response = hf_generator(
                f"Legal area: {legal_area}. Question: {user_question}. Answer:",
                max_length=200,
                num_return_sequences=1
            )
            answer = hf_response[0]["generated_text"]

        except Exception as e:
            st.error(f"⚠️ Error fetching response: {str(e)}")
            answer = "Sorry, something went wrong."

        # Save query and answer
        st.session_state["queries"].append({
            "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "area": legal_area,
            "question": user_question,
            "answer": answer
        })

        # Show Answer
        st.subheader("✅ Answer")
        st.write(answer)

    # Show previous queries
    st.subheader("Your Previous Queries")
    for q in st.session_state["queries"]:
        st.markdown(f"**{q['time']} | {q['area']}**")
        st.markdown(f"Q: {q['question']}")
        st.markdown(f"A: {q['answer']}")
        st.write("---")

elif page == "About":
    st.title("ℹ️ About")
    st.write("This AI-powered tool provides **general legal information**. It does not replace professional legal advice.")

elif page == "Legal Cases":
    st.title("📚 Legal Cases")
    st.write("Here you could display famous legal cases, summaries, or allow uploading case documents for analysis.")
