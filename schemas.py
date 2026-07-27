from pydantic import BaseModel, Field

class ChatRequest(BaseModel):
    query: str = Field(description="User's question")

class ChatResponse(BaseModel):
    output : str = Field(description="User's response.")