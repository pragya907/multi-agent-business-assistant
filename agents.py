import google.generativeai as genai

# Gemini API Key
import os
import google.generativeai as genai

API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=API_KEY)

model = genai.GenerativeModel("gemini-3.5-flash")


def email_agent(email_text):
    prompt = f"""
    Analyze the email.
    Give:
    1. Priority (High/Medium/Low)
    2. Summary
    3. Suggested Reply

    Email:
    {email_text}
    """

    response = model.generate_content(prompt)
    return response.text


def meeting_agent(meeting_notes):
    prompt = f"""
    Summarize the meeting notes.
    Extract action items.

    Notes:
    {meeting_notes}
    """

    response = model.generate_content(prompt)
    return response.text


def task_agent(tasks):
    prompt = f"""
    Prioritize these tasks.

    Tasks:
    {tasks}

    Categorize as:
    High Priority
    Medium Priority
    Low Priority
    """

    response = model.generate_content(prompt)
    return response.text


def report_agent(data_summary):
    prompt = f"""
    Analyze business data.

    Generate:
    1. Insights
    2. Trends
    3. Recommendations

    Data:
    {data_summary}
    """

    response = model.generate_content(prompt)
    return response.text

def manager_agent(user_request):
    prompt = f"""
    You are a Business Operations Manager AI.

    Analyze the user's request and provide:

    1. Executive Summary
    2. Key Priorities
    3. Risks
    4. Recommended Actions
    5. Final Decision

    Request:
    {user_request}
    """

    response = model.generate_content(prompt)
    return response.text

def sql_agent(user_question, table_schema):
    prompt = f"""
    You are an expert SQL assistant.

    Convert the user's question into a SQLite SQL query.

    Rules:
    - Use only the given table schema.
    - Return only SQL query.
    - Do not add explanation.
    - Table name is sales.

    Table Schema:
    {table_schema}

    User Question:
    {user_question}
    """

    response = model.generate_content(prompt)
    return response.text.replace("```sql", "").replace("```", "").strip()

def rule_based_sql_agent(user_question):
    q = user_question.lower()

    if "average" in q and "customer" in q:
        return "SELECT ROUND(AVG(Customers), 0) AS Average_Customers FROM sales;"

    elif "highest" in q and "revenue" in q:
        return "SELECT Month, Revenue FROM sales ORDER BY Revenue DESC LIMIT 1;"

    elif "total" in q and "revenue" in q:
        return "SELECT SUM(Revenue) AS Total_Revenue FROM sales;"

    elif "highest" in q and "complaint" in q:
        return "SELECT Month, Complaints FROM sales ORDER BY Complaints DESC LIMIT 1;"

    elif "lowest" in q and "complaint" in q:
        return "SELECT Month, Complaints FROM sales ORDER BY Complaints ASC LIMIT 1;"

    else:
        return None