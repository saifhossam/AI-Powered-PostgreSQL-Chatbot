import os
import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text
from langchain_google_genai import GoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
import re
from dotenv import load_dotenv

# ---------------- CONFIG ----------------
# load environment variables from .env file
load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
DB_URL = os.getenv("DB_URL")

st.set_page_config(page_title="SQL Chatbot", layout="wide")
st.title("Chat with Postgres DB 🐘")

# ---------------- DATABASE ----------------
@st.cache_resource
def get_db_engine():
    return create_engine(DB_URL)

def get_schema():
    engine = get_db_engine()
    query = text("""
        SELECT table_name, column_name
        FROM information_schema.columns
        WHERE table_schema = 'public'
        ORDER BY table_name, ordinal_position;
    """)

    schema = ""
    with engine.connect() as conn:
        result = conn.execute(query)
        current_table = None
        for table, column in result:
            if table != current_table:
                schema += f"\nTable: {table}\n"
                current_table = table
            schema += f"  - {column}\n"
    return schema

# ---------------- LLM ----------------
@st.cache_resource
def load_llm():
    return GoogleGenerativeAI(
        model="models/gemini-2.5-flash",
        api_key=GOOGLE_API_KEY
    )

llm = load_llm()

# ---------------- PROMPTS ----------------
sql_prompt = PromptTemplate(
    input_variables=["schema", "question"],
    template="""
You are an expert PostgreSQL SQL query generator.

Your task is to generate a valid PostgreSQL SELECT query that answers the user's question based ONLY on the provided table schema.

OUTPUT REQUIREMENTS
- Return ONLY the raw SQL query.
- The query MUST be written in a single line.
- Do NOT include explanations.
- Do NOT include comments.
- Do NOT format in markdown.
- Do NOT wrap in ```sql.

DATABASE DIALECT
- Database system: PostgreSQL.
- Use PostgreSQL syntax ONLY.
- Do NOT use SQLite functions such as STRFTIME.
- When extracting date parts, use: EXTRACT(YEAR FROM column).
- When using EXTRACT, ALWAYS cast the column using ::timestamp.

TABLE SCHEMA
{schema}

USER QUESTION
{question}

CRITICAL SQL FORMATTING RULES
- Always wrap table names in double quotes.
- Always wrap column names in double quotes.
- Do NOT use table aliases.
- If selecting columns with identical names from different tables, ALWAYS use column aliases.
- Column aliases MUST be wrapped in double quotes.
- Do NOT use column aliases inside GROUP BY.
- Repeat the full expression inside GROUP BY instead of using the alias.

STRICT QUERY RULES
- Only generate "SELECT" queries.
- Never generate INSERT, UPDATE, DELETE, DROP, ALTER, or TRUNCATE.
- Use ONLY the tables and columns provided in the schema.
- Do NOT hallucinate tables or columns.
- Always use proper JOIN conditions based on foreign keys.
- If aggregation is required, use GROUP BY correctly.
- If the query may return many rows, add LIMIT 20 at the end.
- Do NOT add LIMIT 20 if the query already contains LIMIT 1.
- If a required column does not exist in the schema, return:
  ERROR: Column not found in schema.
"""
)

nl_prompt = PromptTemplate(
    input_variables=["question", "data"],
    template="""
User Question:
{question}

SQL Result:
{data}

Answer the question in natural language.
If the result is empty, say:
"The data does not provide a clear answer."
"""
)

# ---------------- CHAINS ----------------
sql_chain = sql_prompt | llm
nl_chain = nl_prompt | llm

# ---------------- HELPERS ----------------
def clean_sql(sql: str) -> str:
    sql = re.sub(r"```sql", "", sql, flags=re.IGNORECASE)
    sql = re.sub(r"```", "", sql)
    return sql.strip()

# ---------------- APP ----------------
schema = get_schema()

user_question = st.text_input("Ask a question about the database:")

if st.button("Get Answer") and user_question:
    sql_query = clean_sql(
        sql_chain.invoke({
            "schema": schema,
            "question": user_question
        })
    )

    st.code(sql_query, language="sql")

    if not sql_query.lower().startswith("select"):
        st.warning("Only SELECT queries are allowed.")
        st.stop()

    try:
        engine = get_db_engine()
        df = pd.read_sql(sql_query, engine)
        st.dataframe(df)
    except Exception as e:
        st.error(f"SQL Error: {e}")
        st.stop()

    answer = nl_chain.invoke({
        "question": user_question,
        "data": df.to_string(index=False)
    })

    st.markdown(f"### 🧠 Answer\n{answer}")
