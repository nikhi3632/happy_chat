from fastapi import FastAPI
from contextlib import asynccontextmanager
from routes.app import router as app_router
from routes.confidant import router as confidant_router
from routes.voice import router as voice_router
from services.services import get_tts_model, get_stt_model  # Triggers model loading on app start
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
import uvicorn
import os
from dotenv import load_dotenv
load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Preloading TTS and STT models...")
    _ = get_tts_model
    _ = get_stt_model
    print("Models loaded and ready!")
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(GZipMiddleware, minimum_size=1000)  # Enable gzip for responses larger than 1KB

app.include_router(app_router)
app.include_router(confidant_router)
app.include_router(voice_router)

if __name__ == "__main__":
    host = os.getenv("HOST", "127.0.0.1")
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host=host, port=port)
