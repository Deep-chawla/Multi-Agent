from app.agents.base_agent import BaseAgent
from app.prompt.general_prompt import GENERAL_PROMPT
from app.tools.registry import SHARED_TOOLS
from langchain_core.messages import ToolMessage

class GeneralAgent(BaseAgent):
    def __init__(self, llm):
        super().__init__(
            llm=llm,
            system_prompt=GENERAL_PROMPT,
            tools=SHARED_TOOLS  
        )



      

   