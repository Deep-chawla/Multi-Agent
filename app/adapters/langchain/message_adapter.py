from langchain_core.messages import (
    AIMessage,
    BaseMessage,
    HumanMessage,
    SystemMessage,
)

from app.conversation.models.message import Message


class LangChainMessageAdapter:
    """
    Converts domain Message objects into LangChain messages.
    """

    ROLE_MAPPING = {
        "user": HumanMessage,
        "assistant": AIMessage,
        "system": SystemMessage,
    }

    @classmethod
    def to_langchain(cls,messages: list[Message],) -> list[BaseMessage]:
        """
        Convert domain messages to LangChain messages.
        """

        converted_messages: list[BaseMessage] = []

        for message in messages:

            message_class = cls.ROLE_MAPPING.get(message.role)

            if message_class is None:
                continue

            converted_messages.append(
                message_class(
                    content=message.content
                )
            )

        return converted_messages