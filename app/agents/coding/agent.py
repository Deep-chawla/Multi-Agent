from app.agents.base_agent import BaseAgent
from app.prompt.coding_prompt import CODING_PROMPT


class CodingAgent(BaseAgent):

    def __init__(self, llm):

        super().__init__(
            llm=llm,
            system_prompt=CODING_PROMPT
        )