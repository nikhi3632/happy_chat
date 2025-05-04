import httpx
from tenacity import retry, stop_after_attempt, wait_exponential, before_sleep_log
from fastapi import HTTPException
from typing import Dict, Any, List
from config import Config
from utils import parse_streaming_response, extract_text_from_chunks
from models import Chat, ChatResponse

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ConfidantClient:
    def __init__(self, api_key: str = Config.API_KEY, base_url: str = Config.BASE_URL):
        self.api_key = api_key
        self.api_url = f"{base_url}/chat/completions"

    def prepare_headers(self, conversation_id: str) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "conversation_id": conversation_id,
            "conversation-id": conversation_id
        }

    def prepare_payload(self, user_input: str, model: str) -> Dict[str, Any]:
        return {
            "model": model,
            "messages": [{"role": "user", "content": user_input}],
            "temperature": 0.7,
            "stream": True
        }

    @retry(
        stop=stop_after_attempt(5),  # Retry up to 5 times
        wait=wait_exponential(min=1, max=10),  # Exponential backoff between retries
        before_sleep=before_sleep_log(logger, logging.INFO),  # Log before each retry
    )
    async def send_request(self, headers: Dict[str, str], payload: Dict[str, Any]) -> List[Dict[str, Any]]:
        try:
            async with httpx.AsyncClient() as client:
                async with client.stream("POST", 
                                        self.api_url, 
                                        headers=headers, 
                                        json=payload) as response:
                    response.raise_for_status()
                    return await parse_streaming_response(response)
        except httpx.HTTPStatusError as exc:
            raise HTTPException(status_code=exc.response.status_code, detail=f"Confidant error: {exc.response.text}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

    async def chat_response(self, chat: Chat) -> ChatResponse:
        headers = self.prepare_headers(chat.conversation_id)
        payload = self.prepare_payload(chat.user_input, chat.model)
        parsed_response = await self.send_request(headers, payload)
        message_text = extract_text_from_chunks(parsed_response)
        return ChatResponse(
            input=chat.user_input,
            output=message_text,
            confidant_response=parsed_response
        )
