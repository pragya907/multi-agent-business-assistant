from database import save_dataframe_to_db, run_sql_query
import pandas as pd
import streamlit as st
from agents import (
    email_agent,
    meeting_agent,
    task_agent,
    report_agent,
    manager_agent,
    sql_agent,
    rule_based_sql_agent
)

st.set_page_config(
    page_title="Multi-Agent Business Operations Assistant",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Multi-Agent Business Operations Assistant")

agent_choice = st.sidebar.selectbox(
    "Select Agent",
    [
    "Email Agent",
    "Meeting Agent",
    "Task Agent",
    "Report Agent",
    "Manager Agent",
    "SQL Agent"
]
)

if agent_choice == "Email Agent":
    st.header("📧 Email Agent")

    email_text = st.text_area(
        "Email Content"
    )

    if st.button("Analyze Email"):
        if email_text:
            result = email_agent(email_text)
            st.write(result)

elif agent_choice == "Meeting Agent":
    st.header("📝 Meeting Agent")

    meeting_notes = st.text_area(
        "Meeting Notes"
    )

    if st.button("Summarize Meeting"):
        if meeting_notes:
            result = meeting_agent(meeting_notes)
            st.write(result)

elif agent_choice == "Task Agent":
    st.header("✅ Task Prioritization Agent")

    tasks = st.text_area(
        "Enter Tasks"
    )

    if st.button("Prioritize Tasks"):
        if tasks:
            result = task_agent(tasks)
            st.write(result)

elif agent_choice == "Report Agent":
    st.header("📊 Business Report Agent")

    uploaded_file = st.file_uploader(
        "Upload CSV or Excel File",
        type=["csv", "xlsx"]
    )

    business_data = st.text_area("Or Business Data Summary")

    if uploaded_file is not None:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        st.subheader("📄 Uploaded Data Preview")
        st.dataframe(df.head())

        data_summary = df.describe(include="all").to_string()

        if st.button("Analyze Uploaded File"):
            result = report_agent(data_summary)
            st.write(result)

    if st.button("Generate Insights from Text"):
        if business_data:
            result = report_agent(business_data)
            st.write(result)

elif agent_choice == "Manager Agent":

    st.header("🧠 Manager Agent")

    user_request = st.text_area("Describe Business Situation")

    if st.button("Analyze Business"):
        if user_request:
            result = manager_agent(user_request)
            st.write(result)
elif agent_choice == "SQL Agent":
    st.header("🗄️ Natural Language SQL Agent")

    uploaded_file = st.file_uploader(
        "Upload CSV/Excel file to create SQL table",
        type=["csv", "xlsx"]
    )

    if uploaded_file is not None:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        st.subheader("Data Preview")
        st.dataframe(df)

        save_dataframe_to_db(df, "sales")
        st.success("Data saved into SQLite database table: sales")

        table_schema = str(df.dtypes)

        user_question = st.text_input("Ask a question about your data")

        if st.button("Generate SQL and Answer"):
            if user_question:
                query = rule_based_sql_agent(user_question)

                if query is None:
                    query = sql_agent(user_question, table_schema)

                st.subheader("Generated SQL Query")
                st.code(query, language="sql")

                result = run_sql_query(query)

                st.subheader("Answer")
                st.dataframe(result)
            else:
                st.warning("Please enter a question first.")
    else:
        st.info("Please upload a CSV or Excel file first.")
