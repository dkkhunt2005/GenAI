from dotenv import load_dotenv
load_dotenv()

import streamlit as st

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser


llm = ChatGoogleGenerativeAI(model='gemini-3.5-flash-lite').bind(
    automatic_function_calling={'disable': True})

st.title('AskBudyy - AI QnA Bot')
st.markdown('My QnA bot with Langchain and Google Gemini!!')

if 'messages' not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    role=message['role']
    content=message['content']
    st.chat_message(role).markdown(content)

query = st.chat_input('Ask Anything....')
if query:
    st.chat_message('user').markdown(query)
    st.session_state.messages.append({'role':'user','content':query})
    chain = llm | StrOutputParser()
    response = chain.invoke(query)
    st.session_state.messages.append({'role':'ai','content':response})
    st.chat_message('ai').markdown(response)