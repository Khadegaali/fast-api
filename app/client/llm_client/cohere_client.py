import os
from cohere import Client

class CohereClient:
    def __init__(self, api_key: str = None):

        self.api_key = api_key or os.getenv("COHERE_API_KEY")
        if not self.api_key:
            raise ValueError("COHERE_API_KEY is not set in environment or passed as argument.")
        self.client = Client(self.api_key)

    def generate_text(self, prompt: str, max_tokens: int = 100):
        
        try:
            response = self.client.chat(
                message=prompt,
                max_tokens=max_tokens,
                temperature=0.7,
                model="command-r-08-2024"  
            )
           
            return response.text
        except Exception as e:
            raise Exception(f"Cohere API Error: {str(e)}")