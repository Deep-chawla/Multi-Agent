from pydantic import BaseModel


class ConversationResponse(BaseModel):
    conversation_id: str



class ConversationDto(BaseModel):
    conversation_id: str
    title: str


class ConversationListResponse(BaseModel):
    conversations: list[ConversationDto]


class MessageDto(BaseModel):
    role: str
    content: str


class ConversationMessagesResponse(BaseModel):
    messages: list[MessageDto]