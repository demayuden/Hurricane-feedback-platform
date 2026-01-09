import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
from pathlib import Path
import os
from passlib.context import CryptContext
import base64
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

# =================================================
# PAGE CONFIG
# =================================================
st.set_page_config(page_title="Hurricane Admin Dashboard", layout="wide")
apply_violet_theme()
# =================================================
# LOAD ENV (from backend/.env)
# =================================================
env_path = Path(__file__).resolve().parent.parent / "backend" / ".env"
load_dotenv(dotenv_path=env_path)

DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL is None:
    st.error("DATABASE_URL not found. Check environment configuration.")
    st.stop()

engine = create_engine(DATABASE_URL)

# =================================================
# PASSWORD CONTEXT
# =================================================
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

# =================================================
# AUTH FUNCTIONS
# =================================================
def authenticate(email, password):
    query = text("""
        SELECT password_hash
        FROM admin_users
        WHERE email = :email
    """)
    with engine.connect() as conn:
        result = conn.execute(query, {"email": email}).fetchone()

    if result is None:
        return False

    return pwd_context.verify(password, result[0])

# =================================================
# SESSION STATE
# =================================================
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# =============================
# LOGIN PAGE (BRANDED)
# =============================
if not st.session_state.authenticated:

    st.markdown("<br><br>", unsafe_allow_html=True)

    # Centered layout
    left, center, right = st.columns([1, 1, 1])

    with center:
        logo_path = Path(__file__).parent / "assets" / "hurricane_logo.webp"
        
    with open(logo_path, "rb") as f:
        data = base64.b64encode(f.read()).decode()

        st.markdown(
            f"""
            <div style="text-align:center;">
                <img src="data:image/webp;base64,{data}" width="180">
            </div>
            """,
            unsafe_allow_html=True
        )


        # Company name
        st.markdown(
            "<h3 style='text-align:center; margin-bottom:4px;'>Hurricane Admin Portal</h3>",
            unsafe_allow_html=True
        )

        # Tagline (italic)
        st.markdown(
            """
            <p style='text-align:center; font-style:italic; color:gray; margin-top:0;'>
            Synergizing Systems, Shielding Futures for a Resilient Tomorrow
            </p>
            """,
            unsafe_allow_html=True
        )

        st.markdown("<br>", unsafe_allow_html=True)

        email = st.text_input("Email address")
        password = st.text_input("Password", type="password")

        if st.button("Sign in"):
            if authenticate(email, password):
                st.session_state.authenticated = True
                st.success("Login successful.")
                st.rerun()
            else:
                st.error("Invalid email or password.")

    st.stop()

# =================================================
# SIDEBAR
# =================================================
st.sidebar.title("Hurricane")
st.sidebar.caption("Admin Dashboard")

if st.sidebar.button("Logout"):
    st.session_state.authenticated = False
    st.rerun()

# =================================================
# ADMIN DASHBOARD
# =================================================
st.title("Employee Feedback Dashboard")

query = text("""
    SELECT
        q1, q2, q3, q4, q5, q6,
        sentiment,
        created_date
    FROM feedback
    ORDER BY created_date DESC
""")

df = pd.read_sql_query(query, engine)

if df.empty:
    st.warning("No feedback has been submitted yet.")
    st.stop()

# =================================================
# METRICS
# =================================================
st.subheader("Overview")

col1, col2 = st.columns(2)
col1.metric("Total feedback received", len(df))
col2.metric("Negative sentiment count", int((df["sentiment"] == "NEGATIVE").sum()))

# =================================================
# CHARTS
# =================================================
st.subheader("Sentiment distribution")
st.bar_chart(df["sentiment"].value_counts())

# =================================================
# TABLE
# =================================================
st.subheader("Anonymous feedback responses")
st.dataframe(df, width="stretch")
