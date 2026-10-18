from dotenv import load_dotenv
load_dotenv()

from langchain_groq import ChatGroq
#from langchain_core.output_parsers import StrOutputParser
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain_core.tools import tool
import streamlit as st

#query = input("User: ")

search = GoogleSerperAPIWrapper()
llm = ChatGroq(model='openai/gpt-oss-20b')

#parser = StrOutputParser()

if 'memory' not in st.session_state:
    st.session_state.memory = InMemorySaver()
memory = st.session_state.memory

st.title('ChatBot')
st.markdown('Ask Anything To The Bot')

agent = create_agent(
    model = llm,
    tools = [search.run],
    system_prompt='Work as researcher and give the answers of the user efficiently and in formated way and you name is Dk''s personal agent',
    checkpointer=memory
)

#chain = agent | parser

query = st.chat_input('Ask Anything....')

if 'messages' not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    role = message['role']
    content = message['content']
    st.chat_message(role).markdown(content)

if query:
    #if query.lower() in ['break','quite','done','exit']:
     #   print('Good Bye!!!')
      #  break
    st.chat_message('user').markdown(query)
    st.session_state.messages.append({'role':'user','content':query})
    response = agent.invoke(
        {'messages':[{'role':'user','content':query}]},
        {'configurable':{'thread_id':'a1'}}
        )
    st.session_state.messages.append({'role':'ai','content':response['messages'][-1].content})
    st.chat_message('ai').markdown(response['messages'][-1].content)
   # print('AI: ',response['messages'][-1].content)