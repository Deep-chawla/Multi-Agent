from langchain_groq import ChatGroq
from app.config.settings import settings
from groq import Groq
import instructor
from langchain_core.messages import SystemMessage,AIMessage,HumanMessage


class GroqProvider:

    def __init__(self,model:str="openai/gpt-oss-120b"):
        self.client = ChatGroq(
            api_key=settings.GROQ_API_KEY,
            model=model,
            temperature=settings.TEMPERATURE,
            max_tokens=settings.MAX_TOKENS,
        )

        # Instructor client
        groq_client = Groq(
            api_key=settings.GROQ_API_KEY
        )

        self.structured_client = instructor.from_groq(
            groq_client
        )

    # ---------- Sync ----------

    def invoke(self, messages):
        return self.client.invoke(messages)

    def stream(self, messages):
        for chunk in self.client.stream(messages):
            yield chunk

    # ---------- Async ----------

    async def ainvoke(self, messages):
        return await self.client.ainvoke(messages)

    async def astream(self, messages):
        async for chunk in self.client.astream(messages):
            yield chunk

    #-----------Structured------------
    def invoke_structured(self,messages,response_model):

        formatted_messages = []

        for message in messages:

            if isinstance(message, SystemMessage):
                role = "system"

            elif isinstance(message, HumanMessage):
                role = "user"

            elif isinstance(message, AIMessage):
                role = "assistant"

            else:
                continue

            formatted_messages.append(
                {
                    "role": role,
                    "content": message.content,
                }
            )

        return self.structured_client.chat.completions.create(
            model=settings.SUPERVISOR_MODEL,
            response_model=response_model,
            messages=formatted_messages,
        )