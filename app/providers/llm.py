from langchain_groq import ChatGroq
from app.config.settings import settings


class GroqProvider:

    def __init__(self):
        self.client = ChatGroq(
            api_key=settings.GROQ_API_KEY,
            model=settings.MODEL_NAME,
            temperature=settings.TEMPERATURE,
            max_tokens=settings.MAX_TOKENS,
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