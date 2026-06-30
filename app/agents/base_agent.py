from abc import ABC
from langchain_core.messages import BaseMessage, SystemMessage


class BaseAgent(ABC):
    """
    Base class for all AI agents.
    Responsibilities:
    - Add the system prompt
    - Communicate with the LLM
    - Support normal and streaming responses
    Conversation history is managed by LangGraph.
    """

    def __init__(self, llm, system_prompt):
        self.llm = llm
        self.system_prompt = system_prompt

    def _build_messages(self, messages: list[BaseMessage]) -> list[BaseMessage]:
        """
        Prepend the system prompt to the conversation.
        """
        return [
            SystemMessage(content=self.system_prompt),
            *messages
        ]

    def invoke(self, messages: list[BaseMessage]):
        """
        Returns the complete AIMessage.
        """
        final_messages = self._build_messages(messages)
        response = self.llm.invoke(final_messages)
        return response

    def stream(self, messages: list[BaseMessage]):
        """
        Streams AIMessage chunks.
        """
        final_messages = self._build_messages(messages)
        for chunk in self.llm.stream(final_messages):
            yield chunk