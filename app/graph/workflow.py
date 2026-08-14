from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

from app.graph.state import GraphState
from app.graph.nodes import GraphNodes
from app.graph.lang_route import route


class AgentWorkflow:
    def __init__(self, application):
        self.nodes = GraphNodes(application)
        self.builder = StateGraph(GraphState)
        self._build_graph()
        self.graph = self.builder.compile()

    def _build_graph(self):

        # Register Nodes
        self.builder.add_node("supervisor",self.nodes.supervisor)
        self.builder.add_node("general",self.nodes.general)
        self.builder.add_node("coding",self.nodes.coding)
        self.builder.add_node("research",self.nodes.research)
        self.builder.add_node("scheduler", self.nodes.scheduler)
        self.builder.add_node("final_response",self.nodes.final_response)
        self.builder.add_node("knowledge", self.nodes.knowledge)

        # Start -> Supervisor
        self.builder.add_edge(START,"supervisor")
        # self.builder.add_edge("supervisor","dispatcher")
        self.builder.add_edge("supervisor", "scheduler")

        # Conditional Routing
        self.builder.add_conditional_edges(
            "scheduler",
            route,
        )


        for node in ["general", "coding", "research", "knowledge"]:
            self.builder.add_edge(node, "scheduler")

        self.builder.add_edge("final_response",END)