# from langchain.llms import OpenAI
# pip install --upgrade --quiet  langchain langchain-community langchain-experimental
from langchain_community.llms import OpenAI
# from langchain.utilities import SQLDatabase
# from langchain_experimental.sql import SQLDatabaseChain
from langchain_experimental.sql import SQLDatabaseChain
from langchain_community.utilities import SQLDatabase
# from langchain_openai import ChatOpenAI


# from langchain_community.llms import OpenAI, SQLDatabase
# from langchain_community.utilities import SQLDatabase

db = SQLDatabase.from_uri("sqlite:///database.db")
# print(db)
# db = SQLDatabase.from_uri(
#     "sqlite:///database.db"
# )
llm = OpenAI(temperature=0, verbose=True, openai_api_key="")
db_chain = SQLDatabaseChain.from_llm(llm, db, verbose=True)


