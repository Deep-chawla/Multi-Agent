from app.agents.general.agent import GeneralAgent
from app.memory.conversationalMemory import ChatMemory 
# from app.prompt.general_prompt import SYSTEM_PROMPT
from app.providers.llm import GroqProvider
from app.agents.coding.agent import CodingAgent
from app.agents.superviser.agent import SupervisorAgent


class Application:

    def __init__(self):
        self.llm = GroqProvider()

        self.shared_memory = ChatMemory()
        self.general_agent = GeneralAgent(
            llm=self.llm,
            memory=self.shared_memory,
        )

        self.coding_agent = CodingAgent(
            llm=self.llm,
            memory=self.shared_memory
        )
        self.super_visor = SupervisorAgent(
            llm = self.llm
        )

def start_application():
    return Application()