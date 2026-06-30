from app.providers.llm import GroqProvider

from app.agents.general.agent import GeneralAgent
from app.agents.coding.agent import CodingAgent
from app.agents.superviser.agent import SupervisorAgent

from app.graph.workflow import AgentWorkflow


class Application:

    def __init__(self):

        # LLM
        self.llm = GroqProvider()

        # Agents
        self.general_agent = GeneralAgent(llm=self.llm)

        self.coding_agent = CodingAgent(llm=self.llm)

        self.supervisor = SupervisorAgent(llm=self.llm)

        # LangGraph Workflow
        self.workflow = AgentWorkflow(self)


def start_application():
    return Application()