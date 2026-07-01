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
        self.graph = self.builder.compile(
            checkpointer=MemorySaver()
        )

    def _build_graph(self):

        # Register Nodes
        self.builder.add_node("supervisor",self.nodes.supervisor)
        self.builder.add_node("general",self.nodes.general)
        self.builder.add_node("coding",self.nodes.coding)
        self.builder.add_node("research",self.nodes.research)

        # Start -> Supervisor
        self.builder.add_edge(START,"supervisor")

        # Conditional Routing
        self.builder.add_conditional_edges(
            "supervisor",
            route,
            {
                "general": "general",
                "coding": "coding",
                "research": "research"
            }
        )

        # Finish
        self.builder.add_edge("general",END)
        self.builder.add_edge("research",END)

        self.builder.add_edge("coding",END)