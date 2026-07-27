import os
import streamlit as st
import pandas as pd
import plotly.express as px
from qdrant_client import QdrantClient
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Enterprise HR Dashboard", page_icon="🏢", layout="wide")

# Configure tabs
tab_analytics, tab_copilot = st.tabs(["📊 HR Analytics Dashboard", "🤖 AI Data Engineering Copilot"])

# --- TAB 1: ANALYTICS ---
with tab_analytics:
    st.header("Enterprise HR Datamarts (Gold Layer)")
    
    base_dir = os.path.dirname(os.path.dirname(__file__))
    gold_dir = os.path.join(base_dir, 'data', 'gold')
    
    try:
        dept_df = pd.read_parquet(os.path.join(gold_dir, 'department_summary.parquet'))
        att_df = pd.read_parquet(os.path.join(gold_dir, 'attendance_summary.parquet'))
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Employees", dept_df['headcount'].sum())
        col2.metric("Total Payroll", f"${dept_df['total_salary'].sum():,.2f}")
        col3.metric("Avg Attendance Days", f"{att_df['days_present'].mean():.1f} days")
        
        st.subheader("Headcount by Department")
        fig1 = px.bar(dept_df, x='department', y='headcount', color='department')
        st.plotly_chart(fig1, use_container_width=True)
        
        st.subheader("Department Payroll Costs")
        fig2 = px.pie(dept_df, values='total_salary', names='department', hole=0.4)
        st.plotly_chart(fig2, use_container_width=True)
        
    except Exception as e:
        st.warning("Data not found. Please run the pipeline first to generate the Gold layer data.")

# --- TAB 2: COPILOT ---
with tab_copilot:
    st.header("Ask the HR Pipeline AI")
    st.markdown("I have read your entire Medallion architecture codebase. Ask me anything!")
    
    # Init Groq
    groq_api_key = os.getenv("GROQ_API_KEY")
    groq_client = Groq(api_key=groq_api_key) if groq_api_key else None
    
    if not groq_client:
        st.error("Missing GROQ_API_KEY in .env")
        st.stop()

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("How does the Silver layer handle deduplication?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            with st.spinner("Generating answer..."):
                try:
                    stream = groq_client.chat.completions.create(
                        messages=[
                            {"role": "system", "content": "You are a senior data engineer explaining the Python Medallion pipeline code. Keep it brief and helpful."},
                            {"role": "user", "content": prompt}
                        ],
                        model="llama-3.1-8b-instant",
                        temperature=0.2,
                        stream=True,
                    )
                    full_response = ""
                    for chunk in stream:
                        if chunk.choices[0].delta.content is not None:
                            full_response += chunk.choices[0].delta.content
                            message_placeholder.markdown(full_response + "▌")
                    message_placeholder.markdown(full_response)
                except Exception as e:
                    full_response = f"Error: {e}"
                    message_placeholder.markdown(full_response)

        st.session_state.messages.append({"role": "assistant", "content": full_response})
