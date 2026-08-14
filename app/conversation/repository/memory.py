from app.conversation.models.conversation import Conversation
from app.conversation.models.message import Message
from app.conversation.repository.base import ConversationRepository


class MemoryConversationRepository(ConversationRepository):

    def __init__(self) -> None:
        self._conversations: dict[str, Conversation] = {}

    def create_conversation(self, conversation: Conversation) -> None:
        self._conversations[conversation.id] = conversation

    def get_conversation(self, conversation_id: str) -> Conversation | None:
        return self._conversations.get(conversation_id)

    def list_conversations(self, user_id: str) -> list[Conversation]:
        return [
            con
            for con in self._conversations.values()
            if con.user_id == user_id
        ]

    def add_message(self,conversation_id: str,message: Message,) -> Message:
        conversation = self.get_conversation(conversation_id)

        if conversation is None:
            raise ValueError(
                f"Conversation '{conversation_id}' does not exist."
            )

        conversation.add_message(message)

        return message

    def get_messages(self, conversation_id: str) -> list[Message]:
        conversation = self.get_conversation(conversation_id)

        if conversation is None:
            raise ValueError(
                f"Conversation '{conversation_id}' does not exist."
            )

        return conversation.messages    

    def delete_conversation(self, conversation_id: str) -> None:
        self._conversations.pop(conversation_id, None)