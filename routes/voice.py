from fastapi import APIRouter, UploadFile, File, HTTPException
from models import Chat
from services.services import get_stt_model
# from services.services import get_tts_model
from clients.confidant_client import ConfidantClient
from config import Config
import io
import base64
from gtts import gTTS
import time

router = APIRouter()
confidant_client = ConfidantClient(Config.API_KEY, Config.BASE_URL)

@router.post("/transcribe")
async def transcribe_audio(audio: UploadFile = File(...)):
    stt_model = get_stt_model()
    try:
        audio_bytes = await audio.read()
        audio_stream = io.BytesIO(audio_bytes)
        segments, _ = stt_model.transcribe(audio_stream)
        transcription = " ".join(segment.text for segment in segments)
        return {"transcription": transcription}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/think-and-respond")
async def think_and_respond(req: Chat):
    try:
        response = await confidant_client.chat_response(req)
        response_text = response.output
        # tts_model = get_tts_model()
        # start = time.time()
        tts = gTTS(text=response_text, lang='en')
        # print("TTS synthesis time:", time.time() - start)
        audio_buffer = io.BytesIO()
        tts.write_to_fp(audio_buffer)
        audio_buffer.seek(0)

        base64_audio = base64.b64encode(audio_buffer.read()).decode("utf-8")
        result = {
            "text": response_text,
            "audio_base64": base64_audio
        }
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
