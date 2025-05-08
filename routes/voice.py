from fastapi import APIRouter, UploadFile, HTTPException, File
from models import Chat
from clients.confidant_client import ConfidantClient
from config import Config
import base64
import httpx
from gtts import gTTS, gTTSError
from io import BytesIO

router = APIRouter()
confidant_client = ConfidantClient(Config.API_KEY, Config.BASE_URL)
beam_client = httpx.AsyncClient(http2=True, timeout=httpx.Timeout(connect=None, read=None, write=None, pool=None))

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

        response_stt = await beam_client.post(
            BEAM_STT_URL,
            headers=beam_headers,
            json=beam_payload
        )
        
        if response_stt.status_code != 200:
            raise HTTPException(status_code=500, detail=f"Whisper Error: {response_stt.text}")

        transcription = response_stt.json().get("text", "")
        result = {"transcription": transcription}
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/think-and-respond")
async def think_and_respond(req: Chat):
    try:
        response = await confidant_client.chat_response(req)
        response_text = response.output

        if req.tts_provider == "coqui-xtts-v2":
            beam_payload = {
                "text": response_text,
                "language": "en",
                "speaker": "Andrew Chipper"
            }
            beam_headers = {
                "Authorization": f"Bearer {Config.BEAM_TOKEN}",
                "Content-Type": "application/json"
            }

            response_tts = await beam_client.post(
                BEAM_TTS_URL,
                headers=beam_headers,
                json=beam_payload
            )

            if response_tts.status_code != 200:
                raise HTTPException(status_code=500, detail=f"TTS Error: {response_tts.text}")

            audio_base64 = response_tts.json().get("audio_base64", "")
        
        elif req.tts_provider == "gtts":
            try:
                tts = gTTS(text=response_text, lang="en")
                buf = BytesIO()
                tts.write_to_fp(buf)
                buf.seek(0)
                audio_bytes = buf.read()
                audio_base64 = base64.b64encode(audio_bytes).decode("utf-8")
            except gTTSError as gtts_err:
                raise HTTPException(status_code=500, detail=f"gTTS Error: {str(gtts_err)}")
        
        else:
            raise HTTPException(status_code=400, detail="Invalid TTS provider")
        
        result = {
            "text": response_text,
            "audio_base64": audio_base64,
            "tts_provider": req.tts_provider
        }
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
