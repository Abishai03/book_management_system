# pip install --upgrade --quiet  langchain langchain-community langchain-experimental
from langchain_community.llms import OpenAI
from langchain_experimental.sql import SQLDatabaseChain
from langchain_community.utilities import SQLDatabase

db = SQLDatabase.from_uri("sqlite:///instance/database.db", include_tables=["book"])
llm = OpenAI(temperature=0, verbose=True, openai_api_key="")
db_chain = SQLDatabaseChain.from_llm(llm, db, verbose=True)


