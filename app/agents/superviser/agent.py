import json

from langchain_core.messages import HumanMessage, SystemMessage,BaseMessage
from app.agents.superviser.schema import SupervisorPlan

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
        try:
            response = self.llm.invoke(messages)
            plan = json.loads(response.content)
            validated = SupervisorPlan.model_validate(plan)
            return validated.model_dump()
        
        except Exception as e:
            print("Supervisor validation failed:", e)

            return {
                "plan": [
                    {
                        "agent": "general",
                        "task": "Answer the user's question."
                    }
                ]
            }

        
# r = SupervisorAgent(llm=None)
# print(r.route("research about LangChain and write simple program with fastapi"))