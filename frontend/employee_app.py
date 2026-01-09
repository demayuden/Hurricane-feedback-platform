import streamlit as st
import requests

st.title("Anonymous Employee Feedback")

category = st.selectbox(
    "Category",
    ["Management", "Workload", "Culture", "Tools", "Suggestions"]
)

message = st.text_area("Your feedback (anonymous)")
urgency = st.checkbox("Urgent")

if st.button("Submit"):
    payload = {
        "category": category,
        "message": message,
        "urgency": urgency
    }
    requests.post("http://localhost:8000/feedback", json=payload)
    st.success("Feedback submitted anonymously")
