from langchain_core.messages import HumanMessage
from app.providers.llm import GroqProvider
from app.agents.base_agent import BaseAgent
from app.prompt.general_prompt import GENERAL_PROMPT

class GeneralAgent(BaseAgent):
    def __init__(self, llm):
        super().__init__(llm,GENERAL_PROMPT)

   