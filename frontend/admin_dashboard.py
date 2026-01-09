import streamlit as st
import pandas as pd
import psycopg2

conn = psycopg2.connect("postgresql://postgres:hurricane123@localhost:5432/feedback_db")
df = pd.read_sql("SELECT * FROM feedback", conn)

st.title("Admin Feedback Dashboard")
st.metric("Total Feedback", len(df))

st.bar_chart(df["sentiment"].value_counts())
st.dataframe(df)
