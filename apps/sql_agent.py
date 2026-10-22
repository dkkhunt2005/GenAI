from dotenv import load_dotenv
load_dotenv()

from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langgraph.checkpoint.memory import InMemorySaver
from langchain.agents import create_agent
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain_core.tools import tool


db = SQLDatabase.from_uri('sqlite:///my_task.db')

db.run("""
    create table if not exists task(
        id integer primary key autoincrement,
        title text not null,
    description text,
    status text check(status in ('pending','in progress','completed'))default 'pending',
    created_at timestamp default current_timestamp);
""")

#print('db table creted successfully')

model = ChatGoogleGenerativeAI(model='gemini-3.5-flash-lite')
toolkit = SQLDatabaseToolkit(db=db,llm=model)
search = GoogleSerperAPIWrapper()
tools = toolkit.get_tools(),[search.run]

system_prompt = """
You are a task management assistant that interacts with sql database that contains 'task':

TASK RULES:
1. Limit the select queries by 10 results max with order by created_at desc
2. after create/update/delete always confirm with select query
3. if user requests list of the tasks then give output in structured table format

CRUD OPERSTIONS:
    CREATE: INSERT INTO task(title,description,status)
    READ: SELECT * FROM task WHERE ... limit 10
    UPDATE: UPDATE task SET status=? WHERE id=? OR title=?
    DELETE: DELETE FROM task WHERE id=? OR title=?

TABLE SCHEMA: id,title,description,status(pending/progress/completed), created_at
"""

@st.cache_resource
def get_agent():
    agent = create_agent(
        model=model,
        tools=tools,
        checkpointer=InMemorySaver(),
        system_prompt=system_prompt
    )
    return agent

agent = get_agent()

st.subheader('TaskBot-Manage Your Tasks')

if 'messages' not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    role = message['role']
    content = message['content']
    st.chat_message(role).markdown(content)

prompt = st.chat_input('Ask me to manage your task..')
if prompt:
    st.chat_message('user').markdown(prompt)
    st.session_state.messages.append({'role':'user','content':prompt})
    with st.chat_message('ai'):
        with st.spinner('Processing...'):
            response = agent.invoke(
                {'messages':[{'role':'user','content':prompt}]},
                {'configurable':{'thread_id':'1'}}
                )
            result = response['messages'][-1].text
            st.markdown(result)
            st.session_state.messages.append({'role':'ai','content':result})