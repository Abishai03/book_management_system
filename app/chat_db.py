import os
# from langchain_community.llms import OpenAI
# from langchain_experimental.sql import SQLDatabaseChain
# from langchain_community.utilities import SQLDatabase
from dotenv import load_dotenv
load_dotenv()
from openai import ChatCompletion, api_key

def get_completion(messages,model="gpt-3.5-turbo"):


    response = ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0,
        api_key=os.getenv('OpenAI')
        )
    return response.choices[0].message["content"]


# # OpenAI_Key = ""
# OpenAI_Key =  os.getenv('OpenAI')
# db = SQLDatabase.from_uri("sqlite:///instance/database.db", include_tables=["book"])
# llm = OpenAI(temperature=0, openai_api_key=OpenAI_Key)
# db_chain = SQLDatabaseChain.from_llm(llm, db)
