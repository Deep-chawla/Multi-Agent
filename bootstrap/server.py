from app.agents.research.agent import ResearchAgent
from app.providers.llm import GroqProvider

from app.agents.general.agent import GeneralAgent
from app.agents.coding.agent import CodingAgent
from app.agents.superviser.agent import SupervisorAgent
from app.agents.research.agent import ResearchAgent
from app.agents.Knowledge.agent import KnowledgeAgent
from app.agents.conversation_title.agent import ConversationTitleAgent

from app.graph.workflow import AgentWorkflow

from app.conversation.repository.memory import MemoryConversationRepository
from app.conversation.repository.postgres import PostgresConversationRepository
from app.database.session import SessionLocal
from app.conversation.service.conversation_service import ConversationService


class Application:

    def __init__(self):
        self.title_llm = GroqProvider("openai/gpt-oss-120b")
        self.general_llm = GroqProvider("openai/gpt-oss-120b")
        self.coding_llm = GroqProvider("openai/gpt-oss-120b")
        self.research_llm = GroqProvider("openai/gpt-oss-120b")
        self.knowledge_llm = GroqProvider("llama-3.1-8b-instant")
        self.supervisor_llm = GroqProvider("openai/gpt-oss-120b")
        self.final_llm = GroqProvider("openai/gpt-oss-120b")

        # Conversation
        self.conversation_repository = PostgresConversationRepository(SessionLocal)
        # self.conversation_repository = MemoryConversationRepository()

        self.conversation_service = ConversationService(
            repository=self.conversation_repository
        )
        self.general_agent = GeneralAgent(llm=self.general_llm)
        self.coding_agent = CodingAgent(llm=self.coding_llm)
        self.research_agent = ResearchAgent(llm=self.research_llm)
        self.knowledge_agent = KnowledgeAgent(llm=self.knowledge_llm)
        self.supervisor = SupervisorAgent(llm=self.supervisor_llm)
        self.conversation_title_agent = ConversationTitleAgent(llm=self.title_llm)

        # LangGraph Workflow
        self.workflow = AgentWorkflow(self)


def start_application():
    return Application()