from app.agents.base_agent import BaseAgent
from app.prompt.knowledge_prompt import KNOWLEDGE_PROMPT
from app.tools.registry import RAG_TOOLS

class KnowledgeAgent(BaseAgent):

    def __init__(self, llm):
        super().__init__(
            llm=llm,
            system_prompt=KNOWLEDGE_PROMPT,
            tools=RAG_TOOLS 
        )