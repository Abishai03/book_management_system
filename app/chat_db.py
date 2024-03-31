import os
from langchain_community.llms import OpenAI
from langchain_experimental.sql import SQLDatabaseChain
from langchain_community.utilities import SQLDatabase
from dotenv import load_dotenv
load_dotenv()
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain.agents import create_sql_agent


OpenAI_Key =  os.getenv('OpenAI')
db = SQLDatabase.from_uri("sqlite:///instance/database.db", include_tables=["book"])
llm = OpenAI(temperature=0, openai_api_key=OpenAI_Key)
db_chain = SQLDatabaseChain.from_llm(llm, db)
