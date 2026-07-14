from langgraph.types import Send

def route(state):

    if not state["ready_steps"]:
        return "final_response"

    return [
        Send(
            step["agent"],
            {
                **state,
                "current_task": step
            }
        )
        for step in state["ready_steps"]
    ]