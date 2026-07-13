from langgraph.types import Send

def route(state):
    return [
        Send(step["agent"], state)
        for step in state["plan"]
    ]