from app.agents.base_agent import BaseAgent
from app.prompt.coding_prompt import CODING_PROMPT


class CodingAgent(BaseAgent):

    def __init__(self, llm, memory):

        super().__init__(
            llm=llm,
            memory=memory,
            system_prompt=CODING_PROMPT
        )