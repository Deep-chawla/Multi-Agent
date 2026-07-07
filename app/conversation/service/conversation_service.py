from app.conversation.repository.base import ConversationRepository
from app.conversation.models.conversation import Conversation
from app.conversation.models.message import Message
from typing import Any
from app.conversation.models.message_role import MessageRole

class ConversationService:

    def __init__(self, repository: ConversationRepository) -> None:
        self._repository = repository

    def _create_conversation(self,user_id: str,title: str = "New Chat",) -> Conversation:
        conversation = Conversation(
            user_id=user_id,
            title=title,
        )

        self._repository.create_conversation(conversation)
        return conversation
    
    def get_conversation(self,conversation_id: str,) -> Conversation | None:
        return self._repository.get_conversation(conversation_id)
    

    def get_or_create_conversation(self,conversation_id: str,user_id: str,) -> Conversation:
        conversation = self._repository.get_conversation(conversation_id)
        if conversation is not None:
            return conversation

        conversation = Conversation(
            id=conversation_id,
            user_id=user_id,
        )

        self._repository.create_conversation(conversation)
        return conversation
    
    def add_user_message(self,conversation_id: str,content: str,) -> Message:

        message = self._create_message(
            conversation_id=conversation_id,
            role=MessageRole.USER,
            content=content,
        )

        return self._repository.add_message(
            conversation_id,
            message,
        )
    
    

    def add_assistant_message(self,conversation_id: str,content: str,agent: str,) -> Message:

        message = self._create_message(
            conversation_id=conversation_id,
            role=MessageRole.ASSISTANT,
            content=content,
            agent=agent,
        )

        return self._repository.add_message(
            conversation_id,
            message,
        )
    



    def _create_message(self,conversation_id: str,role: str,content: str,agent: str | None = None,metadata: dict[str, Any] | None = None,) -> Message:
        return Message(
            conversation_id=conversation_id,
            role=role,
            content=content,
            agent=agent,
            metadata=metadata or {},
        )
    
    def get_history(self,conversation_id: str) -> list[Message]:
        return self._repository.get_messages(conversation_id)
    
    def delete_conversation(self,conversation_id: str) -> None:

        self._repository.delete_conversation(
            conversation_id
        )