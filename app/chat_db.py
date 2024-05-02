import os
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
