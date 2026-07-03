import json

from langchain_core.messages import HumanMessage, SystemMessage,BaseMessage

from app.prompt.super_visor_prompt import SUPER_VISOR_PROMPT
from langchain_groq import ChatGroq
from typing import List


class SupervisorAgent:

    def __init__(self, llm):
        self.llm = llm

    def route(self, question: List[BaseMessage]):

        messages = [
            SystemMessage(content=SUPER_VISOR_PROMPT),
            *question
        ]

        response = self.llm.invoke(messages)

        try:
            plan = json.loads(response.content)
            return plan

        except Exception:
            return {
                "plan": ["general"]
            }
        
# r = SupervisorAgent(llm=None)
# print(r.route("research about LangChain and write simple program with fastapi"))