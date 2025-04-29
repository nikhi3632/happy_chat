from pydantic import BaseModel
from typing import List

class Message(BaseModel):
    role: str
    content: str

class Chat(BaseModel):
    user_input: str
    conversation_id: str
    model: str

class ChatResponse(BaseModel):
    input: str
    output: str
    confidant_response: List[dict]  # Raw parsed chunks as dicts
