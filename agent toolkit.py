from langchain_ollama import ChatOllama
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent

# Connect to DB
db = SQLDatabase.from_uri(
    "postgresql://postgres:XajqWihzsfuATrXRplRmdvtLsjQFMRGx@gondola.proxy.rlwy.net:31883/railway"
)

# Local FREE model
llm = ChatOllama(
    model="llama3",   # or "mistral"
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