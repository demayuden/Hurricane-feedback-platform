import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
from pathlib import Path
import os
from passlib.context import CryptContext

# =================================================
# PAGE CONFIG
# =================================================
st.set_page_config(page_title="Hurricane Admin Dashboard", layout="wide")

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

# =================================================
# LOGIN PAGE (BRANDED)
# =================================================
if not st.session_state.authenticated:

    st.markdown("<br><br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image(
            "frontend/assets/hurricane_logo.webp",
            use_container_width=True
        )

        st.markdown(
            """
            <h2 style='text-align:center;'>Hurricane Admin Portal</h2>
            <p style='text-align:center; color:gray;'>
            Anonymous employee feedback for continuous improvement
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
