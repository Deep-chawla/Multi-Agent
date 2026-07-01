from langchain_core.messages import HumanMessage, SystemMessage
from app.agents.base_agent import BaseAgent
from app.prompt.research_prompt import RESEARCH_PROMPT
from app.tools.registry import RESEARCH_TOOLS


class ResearchAgent(BaseAgent):

    def __init__(self, llm):
        super().__init__(
            llm=llm,
            system_prompt=RESEARCH_PROMPT,
            tools=RESEARCH_TOOLS
        )

    