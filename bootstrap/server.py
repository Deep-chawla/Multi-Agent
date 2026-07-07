from app.agents.research.agent import ResearchAgent
from app.providers.llm import GroqProvider

from app.agents.general.agent import GeneralAgent
from app.agents.coding.agent import CodingAgent
from app.agents.superviser.agent import SupervisorAgent
from app.agents.research.agent import ResearchAgent
from app.agents.Knowledge.agent import KnowledgeAgent

from app.graph.workflow import AgentWorkflow

from app.conversation.repository.memory import MemoryConversationRepository
from app.conversation.service.conversation_service import ConversationService


class Application:

    def __init__(self):

        # LLM
        self.llm = GroqProvider()

        # Conversation
        self.conversation_repository = MemoryConversationRepository()

        self.conversation_service = ConversationService(
            repository=self.conversation_repository
        )

        # Agents
        self.general_agent = GeneralAgent(llm=self.llm)

        self.coding_agent = CodingAgent(llm=self.llm)

        self.supervisor = SupervisorAgent(llm=self.llm)
        self.research_agent = ResearchAgent(llm=self.llm)
        self.knowledge_agent = KnowledgeAgent(llm=self.llm)

        # LangGraph Workflow
        self.workflow = AgentWorkflow(self)


def start_application():
    return Application()