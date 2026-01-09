import streamlit as st
import requests

def apply_violet_theme():
    st.markdown(
        """
        <style>
        /* Main app background */
        .stApp {
            background-color: #f7f5fb;
        }

        /* Headings */
        h1, h2, h3, h4 {
            color: #4b2e83;
        }

        /* Buttons */
        div.stButton > button {
            background-color: #783EBD;
            color: white;
            border-radius: 6px;
            border: none;
            padding: 0.5em 1.2em;
        }

        div.stButton > button:hover {
            background-color: #4b2375;
            color: white;
        }

        /* Text inputs & text areas */
        textarea, input {
            border-radius: 6px !important;
            border: 1px solid #c6b8e2 !important;
        }

        textarea:focus, input:focus {
            border-color: #5b2d8b !important;
            box-shadow: 0 0 0 0.1rem rgba(91, 45, 139, 0.25) !important;
        }

        /* Success message */
        .stAlertSuccess {
            background-color: #e9e3f5;
            color: #3a1f5d;
            border-left: 4px solid #5b2d8b;
        }

        /* Warning message */
        .stAlertWarning {
            border-left: 4px solid #9b59b6;
        }

        /* Caption text */
        .stCaption {
            color: #6b5a8a;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

st.set_page_config(
    page_title="Employee Feedback Survey",
    layout="centered"
)
apply_violet_theme()

# -----------------------------
# SESSION STATE INIT
# -----------------------------
if "page" not in st.session_state:
    st.session_state.page = "intro"

# =============================
# PAGE 1: INTRO PAGE
# =============================
if st.session_state.page == "intro":

    st.title("💬 Your Feedback Matters")

    st.markdown(
        """
        This is a **100% anonymous employee survey** designed to help **HURRICANE SYSTEMS** grow stronger together.

        ⏱ The survey takes approximately **5–7 minutes**, and your responses will directly support
        improvements in training, processes, and team support.

        ---
        **🗓 Please complete the survey by 15 January.**
        """
    )

    st.markdown(
        "*Thank you for being part of our continuous growth.*"
    )

    st.markdown("---")

    if st.button("➤ Continue to the survey"):
        st.session_state.page = "survey"
        st.rerun()

# =============================
# PAGE 2: SURVEY FORM
# =============================
elif st.session_state.page == "survey":

    # Back button (TOP)
    if st.button("← Back"):
        st.session_state.page = "intro"
        st.rerun()

    st.title("Anonymous Employee Feedback")
    st.caption(
        "All responses are anonymous. No personal or identifying information is collected."
    )

    st.markdown("---")

    q1 = st.text_area(
        "1. What is one thing that has gone well for you or your team recently? (Knowing what works helps us protect those processes)."
    )

    q2 = st.text_area(
        "2. What is the biggest \"pain point\" or obstacle that currently makes your job harder than it needs to be?"
    )

    q3 = st.text_area(
        "3. What is one thing the leadership team could do differently to better support you and your team’s daily success?"
    )

    q4 = st.text_area(
        "4. What resources, tools, or knowledge do you feel you are currently missing that would help you reach the next level in your role?"
    )

    q5 = st.text_area(
        "5. If you were \"CEO\" for a day, what is the first major change you would make to improve the company's culture or operations?"
    )

    q6 = st.text_area(
        "Additional comments (optional)"
    )

    st.markdown("---")

    if st.button("✉ Submit feedback"):
        if not any([q1, q2, q3, q4, q5, q6]):
            st.warning("Please respond to at least one question before submitting.")
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
                "https://hurricane-feedback-platform.onrender.com/feedback",
                json=payload
            )

            if response.status_code == 200:
                st.session_state.page = "thank_you"
                st.rerun()
            else:
                st.error("An unexpected error occurred. Please try again later.")

# =============================
# PAGE 3: THANK YOU PAGE
# =============================
elif st.session_state.page == "thank_you":

    st.title("Thank You")

    st.markdown(
        """
        **Thank you for your feedback.**

        Your response has been submitted successfully and will be reviewed
        in aggregate to help improve our workplace.

        ---
        You may now close this page.
        """
    )

    st.markdown(
        "<p style='color:gray; font-size:0.9em;'>"
        "For anonymity reasons, the survey cannot be submitted more than once per session."
        "</p>",
        unsafe_allow_html=True
    )
