from fastapi import FastAPI
from routes.confidant import router as confidant_router
from routes.app import router as app_router

app = FastAPI()

app.include_router(app_router)
app.include_router(confidant_router)
