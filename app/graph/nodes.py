from langchain_core.messages import HumanMessage,AIMessage

from app.graph.state import GraphState


class GraphNodes:

    def __init__(self, app):
        self.app = app

    def supervisor(self, state: GraphState):
        """
        Create the execution plan.
        """
        question = state["messages"]
        plan = self.app.supervisor.route(question)

        return {
            "plan": plan["steps"],          # or plan["steps"] if you haven't renamed it yet
            "current_step": 0,
            "results": {}
        }

    def dispatcher(self, state: GraphState):
        """
        Decide which agent to execute next.
        """
        plan = state["plan"]
        current_step = state["current_step"]

        if current_step >= len(plan):
            return {
                "next": "final_response"
            }

        return {
            "next": plan[current_step]["agent"]
        }

    def general(self, state: GraphState):
        print("Executing General Agent...")

        messages = self._build_agent_messages(state)
        response = self.app.general_agent.invoke(messages)

        results = dict(state["results"])
        results["general"] = response.content

        return {
            "messages": [response],
            "results": results,
            "current_step": state["current_step"] + 1
        }

    def coding(self, state: GraphState):
        print("Executing Coding Agent...")

        messages = self._build_agent_messages(state)
        response = self.app.coding_agent.invoke(messages)

        results = dict(state["results"])
        results["coding"] = response.content

        return {
            "messages": [response],
            "results": results,
            "current_step": state["current_step"] + 1
        }

    def research(self, state: GraphState):
        print("Executing Research Agent...")

        messages = self._build_agent_messages(state)
        response = self.app.research_agent.invoke(messages)
        results = dict(state["results"])
        results["research"] = response.content

        return {
            "messages": [response],
            "results": results,
            "current_step": state["current_step"] + 1
        }
    

    def final_response(self, state: GraphState):
        """
        Combine all agent outputs into a single response.
        """

        parts = []

        for agent, output in state["results"].items():
            parts.append(output)

        return {
            "messages": [
                AIMessage(content="\n\n".join(parts))
            ]
        }
    
    def _build_agent_messages(self, state: GraphState):
        """
        Build the message for the current agent.
        """
        step = state["plan"][state["current_step"]]
        original_query = state["messages"][0].content
        previous_results = state["results"]

        prompt = f"""

Assigned Task:
{step["task"]}

Previous Agent Results:
{previous_results}
"""
        return [
            HumanMessage(content=prompt)
        ]
