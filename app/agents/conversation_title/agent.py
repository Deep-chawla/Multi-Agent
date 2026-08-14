from langchain_core.messages import HumanMessage, SystemMessage

from app.agents.conversation_title.schema import ConversationTitle
from app.prompt.conversation_title_promopt import TITLE_PROMPT


class ConversationTitleAgent:

    def __init__(self, llm):
        self.llm = llm

    async def generate_title(self, message: str) -> ConversationTitle:

        messages = [
            SystemMessage(content=TITLE_PROMPT),
            HumanMessage(content=message),
        ]

        return await self.llm.ainvoke_structured(
            messages,
            ConversationTitle,
        )