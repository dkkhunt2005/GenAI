from dotenv import load_dotenv
load_dotenv()

from langchain_core.messages import HumanMessage,AIMessage
from langchain_groq import ChatGroq
import streamlit as st
from langchain_core.output_parsers import StrOutputParser

llm=ChatGroq(model='openai/gpt-oss-20b')
st.title('Your Interaction with Groqqqq...')
st.markdown('My QnA bot with Langchain and Groqq!!')

if 'messages' not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    role=message['role']
    content=message['content']
    st.chat_message(role).markdown(content)

question=st.chat_input('User')
if question:
    st.chat_message('human').markdown(question)
    st.session_state.messages.append({'role':'user','content':question})

    chat_history = []
    for msg in st.session_state.messages:
        if msg['role']=='user':
            chat_history.append(HumanMessage(content=msg['content']))
        elif msg['role']=='ai':
            chat_history.append(AIMessage(content=msg['content']))

    
    chain = llm | StrOutputParser()
    response = chain.invoke(chat_history)
   #response=chain.invoke(question)

    st.session_state.messages.append({'role':'ai','content':response})
    st.chat_message('ai').markdown(response)