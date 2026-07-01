from langchain_core.messages import HumanMessage, SystemMessage

from app.prompt.super_visor_prompt import SUPER_VISOR_PROMPT


class SupervisorAgent:
    """
    Routes user requests to the appropriate agent.
    """

    def __init__(self, llm):
        self.llm = llm

    def route(self, question: str) -> str:
        messages = [
            SystemMessage(content=SUPER_VISOR_PROMPT),
            HumanMessage(content=question),
        ]

        response = self.llm.invoke(messages)

        route = response.content.strip().lower()

        if route not in {"general", "coding", "research"}:
            return "general"
        return route