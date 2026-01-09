import streamlit as st
import requests

st.set_page_config(page_title="WorkPulse – Employee Feedback", layout="centered")

# -----------------------------
# SESSION STATE INIT
# -----------------------------
if "page" not in st.session_state:
    st.session_state.page = "intro"

# =============================
# PAGE 1: INTRO PAGE
# =============================
if st.session_state.page == "intro":

    st.title("💬 Your feedback matters")

    st.markdown(
        """
        This is a **100% anonymous team survey** to help **HURRICANE** grow stronger together.

        ⏱ It takes **5–7 minutes**, and your input will **directly shape our training, processes, and team support**.

        ---
        🗓 **Please complete it by 15 January**
        """
    )

    st.markdown("🙏 *Thank you for being part of our growth.*")
    st.markdown("---")

    if st.button("👉 Continue to the survey"):
        st.session_state.page = "survey"
        st.rerun()

# =============================
# PAGE 2: SURVEY FORM
# =============================
elif st.session_state.page == "survey":

    st.title("🗣️ Anonymous Employee Feedback")
    st.caption(
        "Your responses are completely anonymous. "
        "No name, email, IP address, or device information is collected."
    )

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

    q6 = st.text_area(
        "➕ Anything else you would like to share?",
        help="Optional – share anything not covered above."
    )

    st.markdown("---")

    if st.button("📩 Submit feedback"):
        if not any([q1, q2, q3, q4, q5, q6]):
            st.warning("Please answer at least one question before submitting.")
        else:
            payload = {
                "q1": q1,
                "q2": q2,
                "q3": q3,
                "q4": q4,
                "q5": q5,
                "q6": q6
            }

            response = requests.post(
                "http://127.0.0.1:8000/feedback",
                json=payload
            )

            if response.status_code == 200:
                st.success("✅ Thank you. Your anonymous feedback has been submitted.")
                st.balloons()
            else:
                st.error("❌ Something went wrong. Please try again later.")
