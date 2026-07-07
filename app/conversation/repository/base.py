from abc import ABC, abstractmethod

from app.conversation.models.conversation import Conversation
from app.conversation.models.message import Message

class ConversationRepository(ABC):

    @abstractmethod
    def create_conversation(self, conversation: Conversation) -> None:
        pass

    @abstractmethod
    def get_conversation(self, conversation_id: str) -> Conversation | None:
        pass

    @abstractmethod
    def list_conversations(self, user_id: str) -> list[Conversation]:
        pass

    @abstractmethod
    def add_message(self, conversation_id: str, message: Message) -> Message:
        pass

    @abstractmethod
    def get_messages(self, conversation_id: str) -> list[Message]:
        pass

    @abstractmethod
    def delete_conversation(self, conversation_id: str) -> None:
        pass