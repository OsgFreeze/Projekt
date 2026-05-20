from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.routes.endpoints import router as prompt_router

APP_NAME = settings.APP_NAME
APP_VERSION = settings.APP_VERSION
FRONTEND_URLS = settings.FRONTEND_URLS

app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=FRONTEND_URLS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(prompt_router, prefix="/api", tags=["Prompt Processing"])

@app.get("/")
def root():
    return {
        "message": "Backend läuft",
        "version": APP_VERSION,
        "docs": "/docs"    
    }
