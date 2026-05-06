# File: main.py
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from api.notification_router import router as notification_router
from api.notification_router_get import router as notification_get_router
from api.channel_router import router as channel_router

limiter = Limiter(key_func=get_remote_address, default_limits=["2/day"])

app = FastAPI(
    title="Notification Engine API",
    description="Sistema de notificaciones multicanal production-ready generado por M.A.I.I.E. Systems",
    version="1.0.0",
)

app.state.limiter = limiter

@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={
            "error": "Limite de pruebas alcanzado.",
            "mensaje": "Has usado tus 2 intentos de demo. Contacta a ingenieroedissonia@gmail.com para acceso completo.",
            "contacto": "ingenieroedissonia@gmail.com"
        }
    )

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

app.include_router(notification_router, prefix="/api/v1")
app.include_router(notification_get_router, prefix="/api/v1")
app.include_router(channel_router, prefix="/api/v1")

@app.get("/", tags=["Health"])
def root():
    return {"system": "Notification Engine API", "version": "1.0.0", "status": "online", "docs": "/docs", "generated_by": "M.A.I.I.E. Systems"}

@app.get("/health", tags=["Health"])
def health():
    return {"status": "healthy"}
