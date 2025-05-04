from fastapi import APIRouter
from models import Chat, ChatResponse
from clients.confidant_client import ConfidantClient
from config import Config

router = APIRouter()
confidant_client = ConfidantClient(Config.API_KEY, Config.BASE_URL)

@router.post("/confidant/chat", response_model=ChatResponse)
async def get_confidant_response(chat: Chat):
    return await confidant_client.chat_response(chat)

@router.post("/confidant/health", response_model=ChatResponse)
async def confidant_health_check():
    """
    Sends a 'Hello' message to the Confidant API to check if it's responsive.
    Returns the API's response for the health check.
    """
    health_message = Chat(user_input="Hello", conversation_id="healthcheck-123", model=Config.CHAT_MODEL)
    return await confidant_client.chat_response(health_message)

@router.get("/confidant/health", response_model=ChatResponse)
async def health_check_get():
    """
    Hacky non-standard usage for health check using GET method, assuming 'Hello' as the input.
    """
    health_message = Chat(user_input="Hello", conversation_id="healthcheck-123", model=Config.CHAT_MODEL)
    return await confidant_client.chat_response(health_message)
