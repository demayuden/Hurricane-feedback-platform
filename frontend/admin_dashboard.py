from sqlalchemy import create_engine, text
from dotenv import load_dotenv
from pathlib import Path
import os
import pandas as pd
import streamlit as st

# -------------------------------------------------
# Load .env explicitly
# -------------------------------------------------
env_path = Path(__file__).resolve().parent.parent / "backend" / ".env"
load_dotenv(dotenv_path=env_path)

DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL is None:
    st.error("DATABASE_URL not found. Check backend/.env")
    st.stop()

engine = create_engine(DATABASE_URL)

query = text("""
    SELECT
        q1, q2, q3, q4, q5,
        sentiment,
        urgency,
        created_date
    FROM feedback
    ORDER BY created_date DESC
""")

df = pd.read_sql_query(query, engine)
import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
from pathlib import Path
import os

# -----------------------------
# BASIC UI (ALWAYS SHOWS)
# -----------------------------
st.set_page_config(page_title="WorkPulse Admin", layout="wide")
st.title("📊 WorkPulse – Admin Dashboard")
st.write("✅ Admin dashboard loaded")

# -----------------------------
# LOAD ENV (FORCED)
# -----------------------------
env_path = Path(__file__).resolve().parent.parent / "backend" / ".env"
load_dotenv(dotenv_path=env_path)

DATABASE_URL = os.getenv("DATABASE_URL")

st.write("🔍 DATABASE_URL loaded:", DATABASE_URL is not None)

if DATABASE_URL is None:
    st.error("DATABASE_URL not found. Check backend/.env")
    st.stop()

# -----------------------------
# CONNECT DB
# -----------------------------
engine = create_engine(DATABASE_URL)

query = text("""
    SELECT
        q1, q2, q3, q4, q5,
        sentiment,
        urgency,
        created_date
    FROM feedback
    ORDER BY created_date DESC
""")

try:
    df = pd.read_sql_query(query, engine)
    st.success("✅ Data loaded from database")
except Exception as e:
    st.error("❌ Database query failed")
    st.exception(e)
    st.stop()

# -----------------------------
# SHOW RAW DATA (DEBUG VIEW)
# -----------------------------
st.subheader("🧪 Raw Data Preview")
st.write(df)

# -----------------------------
# IF NO DATA
# -----------------------------
if df.empty:
    st.warning("⚠️ No feedback found in database yet.")
    st.stop()

# -----------------------------
# METRICS
# -----------------------------
st.subheader("📈 Overview")

col1, col2, col3 = st.columns(3)
col1.metric("Total Feedback", len(df))
col2.metric("Urgent Issues", int(df["urgency"].sum()))
col3.metric(
    "Negative Feedback",
    int((df["sentiment"] == "NEGATIVE").sum())
)

# -----------------------------
# CHARTS
# -----------------------------
st.subheader("📊 Sentiment Distribution")
st.bar_chart(df["sentiment"].value_counts())

st.subheader("📂 Feedback Table")
st.dataframe(df, width="stretch")

