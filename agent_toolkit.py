import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent

# Set your API key
os.environ["GOOGLE_API_KEY"] = "AIzaSyCYAZINSAUfVi7aMv59aT2nfRzAkwTMHjU"

# Connect to DB
db = SQLDatabase.from_uri(
    "postgresql://postgres:XajqWihzsfuATrXRplRmdvtLsjQFMRGx@gondola.proxy.rlwy.net:31883/railway"
)

# Gemini 2.5 Flash model
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0
)

# Create SQL Agent
agent = create_sql_agent(
    llm=llm,
    db=db,
    verbose=True
)

response = agent.invoke(
    {"input": "What are the top 5 best selling products?"}
)

print(response["output"])