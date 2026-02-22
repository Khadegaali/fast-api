from pydantic import BaseModel

class LLMRequest(BaseModel):
      user_id: int
      message: str

class LLMResponse(BaseModel):
    text: str
