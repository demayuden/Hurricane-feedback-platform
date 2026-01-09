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
st.set_page_config(page_title="WorkPulse Admin", layout="wide")

# =================================================
# LOAD ENV (from backend/.env)
# =================================================
env_path = Path(__file__).resolve().parent.parent / "backend" / ".env"
load_dotenv(dotenv_path=env_path)

DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL is None:
    st.error("DATABASE_URL not found. Check backend/.env")
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
# LOGIN PAGE
# =================================================
if not st.session_state.authenticated:
    st.title("🔐 Admin Login")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if authenticate(email, password):
            st.session_state.authenticated = True
            st.success("Login successful")
            st.rerun()
        else:
            st.error("Invalid email or password")

    st.stop()  # ⛔ block dashboard if not logged in

# =================================================
# LOGOUT BUTTON
# =================================================
st.sidebar.button(
    "🚪 Logout",
    on_click=lambda: st.session_state.update({"authenticated": False})
)

# =================================================
# ADMIN DASHBOARD (ONLY AFTER LOGIN)
# =================================================
st.title("📊 WorkPulse – Admin Dashboard")

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
    st.warning("No feedback submitted yet.")
    st.stop()

# -------------------------
# METRICS
# -------------------------
col1, col2= st.columns(2)
col1.metric("Total Feedback", len(df))
col2.metric("Negative Feedback", int((df["sentiment"] == "NEGATIVE").sum()))

# -------------------------
# CHARTS
# -------------------------
st.subheader("📊 Sentiment Distribution")
st.bar_chart(df["sentiment"].value_counts())

# -------------------------
# TABLE
# -------------------------
st.subheader("📝 Anonymous Feedback")
st.dataframe(df, width="stretch")
