from pydantic import BaseModel


# class ChatRequest(BaseModel):
#     user_id: str
#     conversation_id: str
#     message: str


# class ChatResponse(BaseModel):
#     response: str

class SendMessageRequest(BaseModel):
    message: str


class SendMessageResponse(BaseModel):
    response: str