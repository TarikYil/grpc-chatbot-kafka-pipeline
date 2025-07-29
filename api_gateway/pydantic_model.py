from pydantic import BaseModel

class PromptRequest(BaseModel):
    """Model for incoming prompt requests."""
    prompt: str