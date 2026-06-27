from langchain_core.messages import (HumanMessage,AIMessage,BaseMessage)


class ChatMemory:
    """
    Manages conversation history for the current chat session.
    """

    def __init__(self, max_messages: int = 20):
        self.history = []
        self.max_messages = max_messages

    def add_user_message(self, content: str):
        self.history.append(HumanMessage(content=content))

    def add_ai_message(self, content: str):
        self.history.append(AIMessage(content=content))

    def get_messages(self):
        return self.history

    def clear(self):
        self.history = [self.system_prompt]

    def needs_summarization(self):
        # Ignore the initial SystemMessage
        return len(self.history) >= self.max_messages

    def update_with_summary(self, summary: str):

        recent_messages = self.history[-5:]

        self.history = [
            self.system_prompt,
            SystemMessage(
                content=f"Previous conversation summary:\n\n{summary}"
            ),
            *recent_messages,
        ]