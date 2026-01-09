import streamlit as st
import requests

st.set_page_config(page_title="WorkPulse Feedback", layout="centered")

st.title("🗣️ Anonymous Employee Feedback")
st.caption("Your responses are completely anonymous. No identity or tracking information is collected.")

st.markdown("---")

q1 = st.text_area(
    "1️⃣ What is one thing that has gone well for you or your team recently?",
    help="Knowing what works helps us protect those processes."
)

q2 = st.text_area(
    "2️⃣ What is the biggest pain point or obstacle that makes your job harder than it needs to be?"
)

q3 = st.text_area(
    "3️⃣ What is one thing leadership could do differently to better support your daily success?"
)

q4 = st.text_area(
    "4️⃣ What resources, tools, or knowledge are you currently missing?"
)

q5 = st.text_area(
    "5️⃣ If you were CEO for a day, what is the first major change you would make?"
)

urgent = st.checkbox("🚨 This feedback is urgent")

if st.button("Submit Feedback"):
    if not any([q1, q2, q3, q4, q5]):
        st.warning("Please answer at least one question.")
    else:
        payload = {
            "q1": q1,
            "q2": q2,
            "q3": q3,
            "q4": q4,
            "q5": q5,
            "urgency": urgent
        }
        requests.post("http://127.0.0.1:8000/feedback", json=payload)
        st.success("Thank you. Your anonymous feedback has been submitted.")
