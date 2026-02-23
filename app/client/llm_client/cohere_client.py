import os
from cohere import Client

class CohereClient:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("COHERE_API_KEY")
        if not self.api_key:
            raise ValueError("COHERE_API_KEY is not set in environment or passed as argument.")
        self.client = Client(self.api_key)

    # Chat generation
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

    # Title generation
    def generate_title(self, first_message: str):
        try:
            prompt = f"""Generate a short, concise title (maximum 6 words) for a conversation that starts with this message:

"{first_message}"

Title should be in the same language as the message. Only return the title, nothing else."""

            response = self.client.chat(
                message=prompt,
                max_tokens=50,
                temperature=0.5,
                model="command-r-plus-08-2024"
            )

            title = response.text.strip()

            # Remove quotes if present
            if title.startswith('"') and title.endswith('"'):
                title = title[1:-1]
            if title.startswith("'") and title.endswith("'"):
                title = title[1:-1]

            # Limit to 50 characters
            if len(title) > 50:
                title = title[:47] + "..."
            
            return title or first_message[:50]

        except Exception as e:
            return first_message[:50] if len(first_message) > 50 else first_message

    # Embedding generation
    def get_embedding(self, text: str, model: str = "embed-v4.0") -> list[float]:
        """
        Generate embedding for a given text using Cohere embed-4.
        """
        try:
            response = self.client.embed(
                model=model,
                texts=[text]
            )
            return response.embeddings[0]
        except Exception as e:
            raise Exception(f"Cohere Embedding Error: {str(e)}")