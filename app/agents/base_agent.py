from abc import ABC
from langchain_core.messages import SystemMessage
from app.providers.llm import GroqProvider


class BaseAgent(ABC):
    """
    Base class for all AI agents.

    Handles:
    - LLM communication
    - Conversation memory
    - Streaming responses
    - Normal invoke responses
    """

    def __init__(self,llm,memory,system_prompt):
        self.llm = llm
        self.memory = memory
        self.system_prompt = system_prompt

    def invoke(self, question: str):
        self.memory.add_user_message(question)
        messages = self.memory.get_messages()
        response = self.llm.invoke(messages)
        self.memory.add_ai_message(response.content)
        return response.content

    def stream(self, question: str):
        self.memory.add_user_message(question)

        messages = [
            SystemMessage(content=self.system_prompt),
            *self.memory.get_messages()
        ]
        full_response = ""
        for chunk in self.llm.stream(messages):
            if chunk.content:
                full_response += chunk.content
                yield chunk.content
        self.memory.add_ai_message(full_response)