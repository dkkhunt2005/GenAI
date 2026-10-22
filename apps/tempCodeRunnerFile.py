response = agent.invoke(
        {'messages':[{"role":"user","content":query}]},
        {'configurable':{'thread_id':1}}
        )