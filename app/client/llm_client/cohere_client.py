import os
import json
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

    def generate_title(self, first_message: str):
        try:
            prompt = f"""Generate a short, concise title (maximum 6 words) for a video based on this transcript:

"{first_message[:1000]}"

Title should be in the same language as the transcript. Only return the title, nothing else."""

            response = self.client.chat(
                message=prompt,
                max_tokens=50,
                temperature=0.5,
                model="command-r-plus-08-2024"
            )
            title = response.text.strip()

            if title.startswith('"') and title.endswith('"'):
                title = title[1:-1]
            if title.startswith("'") and title.endswith("'"):
                title = title[1:-1]

            if len(title) > 50:
                title = title[:47] + "..."

            return title or first_message[:50]
        except Exception:
            return first_message[:50]

    def generate_topic(self, transcript: str) -> str:
        try:
            response = self.client.chat(
                message=f"Extract 5-10 single keywords from this video transcript. Return only the keywords separated by commas, no sentences:\n\n{transcript[:3000]}",
                max_tokens=30,
                temperature=0.3,
                model="command-r-08-2024"
            )
            return response.text.strip()
        except Exception:
            return ""

    def get_embedding(self, text: str, input_type: str = "search_document"):
        try:
            response = self.client.embed(
                model="embed-v4.0",
                texts=[text],
                input_type=input_type
            )
            return response.embeddings[0]
        except Exception as e:
            raise Exception(f"Cohere Embedding Error: {str(e)}")

    def analyze_cv(self, cv_text: str) -> dict:
        try:
            response = self.client.chat(
                message=f"""Analyze this CV and return ONLY a JSON object with these exact keys:
- name: full name of the person (string)
- phone: phone number (string)               
- graduation_year: the year of graduation (string)
- education: degree and university name (string)
- technical_skills: comma separated list of technical skills (string)
- experience: list of job titles and companies (string)
- summary: 3-4 sentence professional summary (string)

CV:
{cv_text[:5000]}

Return only valid JSON, no extra text.""",
                max_tokens=600,
                temperature=0.2,
                model="command-r-plus-08-2024"
            )
            text = response.text.strip().replace("```json", "").replace("```", "")
            result = json.loads(text)
            
            skills = result.get("technical_skills", [])
            if isinstance(skills, str):
                result["technical_skills"] = [s.strip() for s in skills.split(",")]

            return result
        except Exception:
            return {
                "name": None,
                "phone": None,
                "graduation_year": None,
                "education": None,
                "technical_skills": [],
                "experience": None,
                "summary": None
            }