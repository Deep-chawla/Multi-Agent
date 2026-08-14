from app.api.schema.conversation import (ConversationResponse, ConversationDto, ConversationListResponse,ConversationMessagesResponse,MessageDto)
from app.api.exceptions.conversation import ConversationNotFoundException


class ConversationAPIService:

    def __init__(self, application):
        self.app = application
        

    def create_conversation(self, user_id: str):
        conversation = (self.app.conversation_service.create_conversation(user_id))
        return ConversationResponse(conversation_id=conversation.id)
    
    
    def list_conversations(self, user_id: str) -> ConversationListResponse:
        conversations = (
            self.app.conversation_service.list_conversations(user_id)
        )
        return ConversationListResponse(
            conversations=[
                ConversationDto(
                    conversation_id=conversation.id,
                    title=conversation.title,
                )
                for conversation in conversations
            ]
        )
    

    def get_messages(self,conversation_id: str,user_id: str | None = None,) -> ConversationMessagesResponse:

        conversation = self._get_owned_conversation(conversation_id, user_id)

        messages = self.app.conversation_service.get_history(
            conversation_id
        )

        return ConversationMessagesResponse(
            messages=[
                MessageDto(
                    role=message.role,
                    content=message.content,
                )
                for message in messages
            ]
        )
    

    def require_conversation(self, conversation_id: str, user_id: str | None = None):
        return self._get_owned_conversation(conversation_id, user_id)

    def _get_owned_conversation(self, conversation_id: str, user_id: str | None):
        """Fetch a conversation and make sure it belongs to user_id.

        A conversation that exists but belongs to someone else is reported
        as 'not found' rather than 'forbidden', so we don't leak which
        conversation ids exist to users who don't own them.
        """
        conversation = self.app.conversation_service.get_conversation(
            conversation_id
        )

        if conversation is None:
            raise ConversationNotFoundException(conversation_id)

        if user_id is not None and conversation.user_id != user_id:
            raise ConversationNotFoundException(conversation_id)

        return conversation