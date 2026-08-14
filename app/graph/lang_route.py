from langgraph.types import Send

def route(state):

    executions = dict(state["executions"])
    sends = []

    for execution in executions.values():

        if execution.status != "READY":
            continue

        execution.status = "RUNNING"

        sends.append(
            Send(
                execution.step.agent,
                {
                    **state,
                    "current_task": execution.step,
                    "executions": executions,
                }
            )
        )

    if not sends:
        return "final_response"

    return sends