import os
from langchain_community.llms import OpenAI
from langchain_experimental.sql import SQLDatabaseChain
from langchain_community.utilities import SQLDatabase
from dotenv import load_dotenv
load_dotenv()
# from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain.agents import create_sql_agent


OpenAI_Key =  os.getenv('OpenAI')
db = SQLDatabase.from_uri("sqlite:///instance/database.db", include_tables=["book"])
llm = OpenAI(temperature=0, openai_api_key=OpenAI_Key) #verbose=True, 
db_chain = SQLDatabaseChain.from_llm(llm, db) #verbose=True


"""
https://github.com/MG-Microsoft/ChatGPT-Tabular-Data/blob/main/Notebook.ipynb
https://medium.com/@VeryFatBoy/quick-tip-using-langchains-sqldatabasetoolkit-with-singlestoredb-a2106d3260f5

db = SQLDatabase.from_uri("sqlite:///../instance/database.db", include_tables=["book"])


llm = OpenAI(
    temperature = 0,
    verbose = False,
    openai_api_key=OpenAI_Key
)

# toolkit = SQLDatabaseToolkit(db=db, llm=ChatOpenAI(temperature=0,openai_api_key=OpenAI_Key))



toolkit = SQLDatabaseToolkit(
    db = db,
    llm = llm
)

agent_executor = create_sql_agent(
    llm = llm,
    toolkit = toolkit,
    verbose = True
)
agent_executor.run("hello ther")

from openai import OpenAI
client = OpenAI()

response = client.chat.completions.create(
  model="gpt-4",
  messages=[
    {
      "role": "system",
      "content": "Given the following SQL tables, your job is to write queries given a user’s request.\n    \n    CREATE TABLE Orders (\n      OrderID int,\n      CustomerID int,\n      OrderDate datetime,\n      OrderTime varchar(8),\n      PRIMARY KEY (OrderID)\n    );\n    \n    CREATE TABLE OrderDetails (\n      OrderDetailID int,\n      OrderID int,\n      ProductID int,\n      Quantity int,\n      PRIMARY KEY (OrderDetailID)\n    );\n    \n    CREATE TABLE Products (\n      ProductID int,\n      ProductName varchar(50),\n      Category varchar(50),\n      UnitPrice decimal(10, 2),\n      Stock int,\n      PRIMARY KEY (ProductID)\n    );\n    \n    CREATE TABLE Customers (\n      CustomerID int,\n      FirstName varchar(50),\n      LastName varchar(50),\n      Email varchar(100),\n      Phone varchar(20),\n      PRIMARY KEY (CustomerID)\n    );"
    },
    {
      "role": "user",
      "content": "Write a SQL query which computes the average total order value for all orders on 2023-04-01."
    }
  ],
  temperature=0.7,
  max_tokens=64,
  top_p=1
)
"""