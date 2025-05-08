from pydantic import BaseModel
from typing import List, Literal

class Message(BaseModel):
    role: str
    content: str

class Chat(BaseModel):
    user_input: str
    conversation_id: str
    model: str
    tts_provider: Literal["coqui-xtts-v2", "gtts"] = "gtts"  # default to gtts

class ChatResponse(BaseModel):
    input: str
    output: str
    confidant_response: List[dict]  # Raw parsed chunks as dicts
