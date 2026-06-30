from app.graph.state import GraphState

def route(state:GraphState):
    return state["next"]