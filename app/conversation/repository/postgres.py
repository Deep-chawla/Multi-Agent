from sqlalchemy.orm import sessionmaker

from app.conversation.models.conversation import Conversation
from app.conversation.models.message import Message
from app.conversation.repository.base import ConversationRepository

from app.database.models.conversation import ConversationEntity
from app.database.models.message import MessageEntity
from sqlalchemy import select

class PostgresConversationRepository(ConversationRepository):

    def __init__(self, session_factory: sessionmaker):
        self._session_factory = session_factory

    def create_conversation(self, conversation: Conversation) -> None:
        with self._session_factory() as db:
            entity = ConversationEntity(
                id = conversation.id,
                user_id=conversation.user_id,
                title=conversation.title,
                created_at=conversation.created_at,
                updated_at=conversation.updated_at,
            )

            db.add(entity)
            db.commit()


    def get_conversation(self,conversation_id: str,) -> Conversation | None:

        with self._session_factory() as db:
            entity = db.scalar(
                select(ConversationEntity).where(
                    ConversationEntity.id == conversation_id
                )
            )

            if entity is None:
                return None

            return Conversation(
                id=entity.id,
                user_id=entity.user_id,
                title=entity.title,
                created_at=entity.created_at,
                updated_at=entity.updated_at,
            )

    def list_conversations(self,user_id: str,) -> list[Conversation]:
        with self._session_factory() as db:

            entities = db.scalars(
                select(ConversationEntity).where(
                    ConversationEntity.user_id == user_id
                )
            ).all()

            conversations = []

            for entity in entities:

                conversations.append(
                    Conversation(
                        id=entity.id,
                        user_id=entity.user_id,
                        title=entity.title,
                        created_at=entity.created_at,
                        updated_at=entity.updated_at,
                    )
                )
            return conversations

    def add_message(self, conversation_id: str, message: Message) -> Message:
        with self._session_factory() as db:
            msg = MessageEntity(
                id=message.id,
                conversation_id=conversation_id,
                role=message.role,
                content=message.content,
                created_at=message.created_at
            )
            db.add(msg)
            db.commit()
            db.refresh(msg)
            return message

    def get_messages(self,conversation_id: str,) -> list[Message]:

        with self._session_factory() as db:
            entities = db.scalars(
                select(MessageEntity).where(
                    MessageEntity.conversation_id == conversation_id
                )
            ).all()

            messages = []

            for entity in entities:

                messages.append(
                    Message(
                        id=entity.id,
                        conversation_id=entity.conversation_id,
                        role=entity.role,
                        content=entity.content,
                        created_at=entity.created_at,
                    )
                )

            return messages

    def delete_conversation(self,conversation_id: str,) -> None:

        with self._session_factory() as db:

            entity = db.get(
                ConversationEntity,
                conversation_id,
            )

            if entity is None:
                return

            db.delete(entity)
            db.commit()