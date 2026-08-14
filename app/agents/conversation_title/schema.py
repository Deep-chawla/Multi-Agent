from pydantic import BaseModel, Field

class ConversationTitle(BaseModel):
    title: str = Field(
        description="A concise conversation title of 3-5 words."
    )