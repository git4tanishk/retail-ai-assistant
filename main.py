
from fastapi import FastAPI

from app.api.routes import router

app = FastAPI(title="Retail AI Assistant API")

app.include_router(router, prefix="/api")


@app.get("/")
def home():
    return {
        "message": "Retail AI Assistant API is running!"
    }


@app.get("/health")
def health():
    return {"status": "ok"}
