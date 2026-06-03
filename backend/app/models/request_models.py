from pydantic import BaseModel

class ProcessPromptRequest(BaseModel):
    text: str