from fastapi import FastAPI
from contextlib import asynccontextmanager
from routes.app import router as app_router
from routes.confidant import router as confidant_router
from routes.voice import router as voice_router
from services.services import get_tts_model, get_stt_model  # Triggers model loading on app start

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Preloading TTS and STT models...")
    _ = get_tts_model
    _ = get_stt_model
    print("Models loaded and ready!")
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(app_router)
app.include_router(confidant_router)
app.include_router(voice_router)
