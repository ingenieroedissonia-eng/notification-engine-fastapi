# File: main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.notification_router import router as notification_router
from api.notification_router_get import router as notification_get_router
from api.channel_router import router as channel_router

app = FastAPI(
    title="Notification Engine API",
    description="Sistema de notificaciones multicanal production-ready generado por M.A.I.I.E. Systems",
    version="1.0.0",
)

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

app.include_router(notification_router, prefix="/api/v1")
app.include_router(notification_get_router, prefix="/api/v1")
app.include_router(channel_router, prefix="/api/v1")

@app.get("/", tags=["Health"])
def root():
    return {"system": "Notification Engine API", "version": "1.0.0", "status": "online", "docs": "/docs"}

@app.get("/health", tags=["Health"])
def health():
    return {"status": "healthy"}