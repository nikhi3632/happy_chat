from fastapi import FastAPI
from routes.app import router as app_router
from routes.confidant import router as confidant_router
from routes.voice import router as voice_router
from routes.voice import beam_client
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi_profiler.profiler import PyInstrumentProfilerMiddleware
import uvicorn
import os
from contextlib import asynccontextmanager

app = FastAPI()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    try:
        yield
    # Shutdown logic
    finally:
        await beam_client.aclose()

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(GZipMiddleware, minimum_size=1000)  # Enable gzip for responses larger than 1KB
app.add_middleware(PyInstrumentProfilerMiddleware)

app.include_router(app_router)
app.include_router(confidant_router)
app.include_router(voice_router)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 9000))
    uvicorn.run("main:app", host='0.0.0.0', port=port)
