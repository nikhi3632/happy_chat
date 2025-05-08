from fastapi import APIRouter, UploadFile, HTTPException, File
from models import Chat
from clients.confidant_client import ConfidantClient
from config import Config
import base64
import httpx

router = APIRouter()
confidant_client = ConfidantClient(Config.API_KEY, Config.BASE_URL)
BEAM_TTS_URL = "https://coqui-xtts-v2-0ce9c9b.app.beam.cloud"
BEAM_STT_URL = "https://faster-whisper-base-db92dd5.app.beam.cloud"

@router.post("/transcribe")
async def transcribe_audio(audio: UploadFile = File(...)):
    try:
        audio_bytes = await audio.read()
        audio_b64 = base64.b64encode(audio_bytes).decode("utf-8")
        beam_payload = {
            "audio_file": audio_b64
        }
        beam_headers = {
            "Authorization": f"Bearer {Config.BEAM_TOKEN}",
            "Content-Type": "application/json"
        }

        async with httpx.AsyncClient(timeout=httpx.Timeout(connect=None, read=None, write=None, pool=None)) as client:
            response_stt = await client.post(
                BEAM_STT_URL,
                headers=beam_headers,
                json=beam_payload
            )
        
        if response_stt.status_code != 200:
            raise HTTPException(status_code=500, detail=f"Whisper Error: {response_stt.text}")

        transcription = response_stt.json().get("text", "")

        return {"transcription": transcription}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/think-and-respond")
async def think_and_respond(req: Chat):
    try:
        response = await confidant_client.chat_response(req)
        response_text = response.output

        beam_payload = {
            "text": response_text,
            "language": "en",
            "speaker": "Andrew Chipper"
        }
        beam_headers = {
            "Authorization": f"Bearer {Config.BEAM_TOKEN}",
            "Content-Type": "application/json"
        }

        async with httpx.AsyncClient(timeout=httpx.Timeout(connect=None, read=None, write=None, pool=None)) as client:
            response_tts = await client.post(
                BEAM_TTS_URL,
                headers=beam_headers,
                json=beam_payload
            )

        if response_tts.status_code != 200:
            raise HTTPException(status_code=500, detail=f"TTS Error: {response_tts.text}")

        audio_base64 = response_tts.json().get("audio_base64", "")

        return {
            "text": response_text,
            "audio_base64": audio_base64
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
