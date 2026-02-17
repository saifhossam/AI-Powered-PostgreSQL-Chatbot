import os
import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import re

# LangChain
from langchain_google_genai import GoogleGenerativeAI
from langchain_core.prompts import (
    PromptTemplate,
    FewShotPromptTemplate
)
from langchain_core.example_selectors import SemanticSimilarityExampleSelector
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

from examples import examples

# ---------------- CONFIG ----------------
load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
DB_URL = os.getenv("DB_URL")

st.set_page_config(page_title="SQL Chatbot (RAG + Few Shot)", layout="wide")
st.title("Chat with Postgres DB 🐘 (Dynamic Few-Shot + RAG)")

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


@st.cache_resource
def load_embeddings():
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )


llm = load_llm()
embeddings = load_embeddings()


# ---------------- RAG FEW SHOT ----------------
@st.cache_resource
def load_example_selector():
    # Create vector store from example questions
    vectorstore = Chroma.from_texts(
        texts=[ex["question"] for ex in examples],
        embedding=embeddings,
        metadatas=examples
    )

    selector = SemanticSimilarityExampleSelector(
        vectorstore=vectorstore,
        k=3  # Number of similar examples to retrieve
    )

    return selector


example_selector = load_example_selector()

example_prompt = PromptTemplate(
    input_variables=["question", "sql"],
    template="""
User Question:
{question}

SQL Query:
{sql}
"""
)

dynamic_prompt = FewShotPromptTemplate(
    example_selector=example_selector,
    example_prompt=example_prompt,
    prefix="""
You are an expert PostgreSQL SQL query generator.

Your task is to generate a valid PostgreSQL SELECT query.

CRITICAL SQL RULES:
- The query MUST be a single line.
- Return ONLY raw SQL.
- No explanations.
- No markdown.
- Only SELECT queries.
- Always wrap table names in double quotes.
- Always wrap column names in double quotes.
- Do NOT use table aliases.
- Use only provided schema.
- Add LIMIT 20 if result may return many rows.
""",
    suffix="""
TABLE SCHEMA:
{schema}

USER QUESTION:
{question}
""",
    input_variables=["schema", "question"]
)

sql_chain = dynamic_prompt | llm


# ---------------- NATURAL LANGUAGE ANSWER ----------------
nl_prompt = PromptTemplate(
    input_variables=["question", "data"],
    template="""
User Question:
{question}

SQL Result:
{data}

Answer the question in natural language.
If empty, say:
"The data does not provide a clear answer."
"""
)

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

    # Generate SQL using dynamic few-shot RAG
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

    # Natural language answer
    answer = nl_chain.invoke({
        "question": user_question,
        "data": df.to_string(index=False)
    })

    st.markdown(f"### 🧠 Answer\n{answer}")
