from app.graph.state import GraphState


class GraphNodes:

    def __init__(self, app):
        self.app = app

    def supervisor(self, state: GraphState):
        """
        Route the user query to the correct agent.
        """
        question = state["messages"][-1].content
        route = self.app.supervisor.route(question)
        return {
            "next": route
        }

    def general(self, state: GraphState):
        """
        Execute the General Agent.
        """
        response = self.app.general_agent.invoke(
            state["messages"]
        )
        return {
            "messages": [response]
        }

    def coding(self, state: GraphState):
        """
        Execute the Coding Agent.
        """
        response = self.app.coding_agent.invoke(
            state["messages"]
        )
        return {
            "messages": [response]
        }