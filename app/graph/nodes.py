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
            "plan": plan["plan"],          # or plan["steps"] if you haven't renamed it yet
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
    

    def knowledge(self, state: GraphState):
        print("Executing Knowledge Agent...")

        messages = self._build_agent_messages(state)

        response = self.app.knowledge_agent.invoke(messages)

        results = dict(state["results"])
        results["knowledge"] = response.content

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
    
    from langchain_core.messages import HumanMessage

    def _build_agent_messages(self, state: GraphState):
        step = state["plan"][state["current_step"]]
        previous_results = state["results"]

        original_query = ""

        for message in reversed(state["messages"]):
            if isinstance(message, HumanMessage):
                original_query = message.content
                break

        prompt = f"""
    Your Assigned Task:
    {step["task"]}

    Results from Previous Agents:
    {previous_results}

    Complete only your assigned task.
    """

        return [
            HumanMessage(content=original_query),
            HumanMessage(content=prompt),
        ]