from app.agents.general.agent import GeneralAgent
from app.memory.conversationalMemory import ChatMemory 
from app.prompt.general_prompt import SYSTEM_PROMPT
from app.providers.llm import GroqProvider


class Application:

    def __init__(self):
        self.llm = GroqProvider()

        self.chat_memory = ChatMemory(
            SYSTEM_PROMPT
        )

        self.general_agent = GeneralAgent(
            llm=self.llm,
            memory=self.chat_memory
        )

def start_application():
    return Application()