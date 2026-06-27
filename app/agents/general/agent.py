from langchain_core.messages import HumanMessage
from app.providers.llm import GroqProvider
from app.agents.base_agent import BaseAgent

class GeneralAgent(BaseAgent):
    def __init__(self, llm, memory):
        super().__init__(llm, memory)

   