from app.agents.base_agent import BaseAgent
from app.prompt.coding_prompt import CODING_PROMPT
from app.tools.registry import CODING_TOOLS

from langchain_core.messages import ToolMessage


class CodingAgent(BaseAgent):

    def __init__(self, llm):
        super().__init__(
            llm=llm,
            system_prompt=CODING_PROMPT,
            tools=CODING_TOOLS
        )

    