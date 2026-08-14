class TitleService:

    def __init__(self, llm):
        self.llm = llm

    async def generate_title(self, message: str):
        pass