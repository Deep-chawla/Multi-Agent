from langchain_core.messages import HumanMessage
from app.providers.llm import GroqProvider

class GeneralAgent:
    def __init__(self,memory):
        self.llm = GroqProvider()
        self.memory = memory

    def invoke(self, question: str):
        response = self.llm.invoke(
            [
                HumanMessage(content=question)
            ]
        )
        return response.content

    def stream(self, question: str):
        self.memory.add_user_message(question)

        response = ""

        for chunk in self.llm.stream(self.memory.get_messages()):
            if chunk.content:
                response += chunk.content
                yield chunk.content

        self.memory.add_ai_message(response)