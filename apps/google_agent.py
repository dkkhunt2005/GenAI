from dotenv import load_dotenv
load_dotenv()

from langchain_groq import ChatGroq
from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain.agents import create_agent
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.tools import tool
import streamlit as st

llm = ChatGroq(model='openai/gpt-oss-20b')
search = GoogleSerperAPIWrapper()
memory = MemorySaver()

agent = create_agent(
    model = llm,
    tools = [search.run],
    system_prompt = 'You are an agent and you can search anything from google.',
    checkpointer=memory
)

while True:
    query = input('User: ')
    if query.lower() in ['break','quite','bye','done']:
        print('Good Bye!!!')
        break

    response = agent.invoke(
        {'messages':[{"role":"user","content":query}]},
        {'configurable':{'thread_id':1}}
        )
    print('AI: ', response['messages'][-1].content)