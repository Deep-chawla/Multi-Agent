from google import genai
from PIL import Image
from app.config.settings import settings

class GeminiVision:
    def __init__(self):
        self.client = genai.Client(api_key=settings.GOOGLE_API_KEY)

    def describe_img(self, image_input):
        if isinstance(image_input, str):
            image = Image.open(image_input)
        else:
            image = image_input
        response = self.client.models.generate_content(
            model =  "gemini-2.5-flash",
            contents = [
                """Describe the image in detail.
                Mention:
                - objects
                - people
                - Activities
                - Screenshots
                - Charts
                - Diagrams
                - Important visual information
                - if game try to store status or who wins,score card etc
                """,
                image
            ]
        )
        return response.text

