# Fix: agregar rate limiting y notificacion seed
import os

# 1. Actualizar requirements.txt
req = open('requirements.txt', 'r').read()
if 'slowapi' not in req:
    req = req.strip() + '\nslowapi==0.1.9\n'
    open('requirements.txt', 'w').write(req)
    print('OK: slowapi agregado a requirements.txt')

# 2. Reescribir main.py con rate limiting
main = '''# File: main.py
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
'''
open('main.py', 'w', encoding='utf-8').write(main)
print('OK: main.py con rate limiting')

# 3. Agregar notificacion seed al InMemoryNotificationRepository
f = open('infrastructure/repositories/in_memory_notification_repository.py', 'r', encoding='utf-8')
c = f.read()
f.close()

c = c.replace(
    '        self._notifications: Dict[UUID, Notification] = {}',
    '''        from uuid import UUID
        from datetime import datetime
        from core.notification import NotificationStatus
        seed_id = UUID("00000000-0000-0000-0000-000000000001")
        seed = Notification(
            id=seed_id,
            recipient="demo@maiie-systems.com",
            message="Notificacion de demo generada por M.A.I.I.E. Systems",
            status=NotificationStatus.SENT,
            created_at=datetime(2026, 1, 1, 0, 0, 0),
            updated_at=datetime(2026, 1, 1, 0, 0, 0),
        )
        self._notifications: Dict[UUID, Notification] = {seed_id: seed}'''
)

open('infrastructure/repositories/in_memory_notification_repository.py', 'w', encoding='utf-8').write(c)
print('OK: seed notificacion agregada')

# 4. Agregar decorator rate limit al POST
f = open('api/notification_router.py', 'r', encoding='utf-8')
c = f.read()
f.close()

if 'limiter' not in c:
    c = 'from slowapi import Limiter\nfrom slowapi.util import get_remote_address\nfrom fastapi import Request\n' + c
    c = c.replace(
        '@router.post("/", response_model=Notification, status_code=status.HTTP_201_CREATED)\nasync def create_notification(',
        '@router.post("/", response_model=Notification, status_code=status.HTTP_201_CREATED)\n@limiter.limit("2/day")\nasync def create_notification(request: Request,'
    )
    # Agregar limiter instance
    c = c.replace(
        'router = APIRouter(prefix="/notifications", tags=["notifications"])',
        'router = APIRouter(prefix="/notifications", tags=["notifications"])\nlimiter = Limiter(key_func=get_remote_address)'
    )

open('api/notification_router.py', 'w', encoding='utf-8').write(c)
print('OK: rate limiting en POST')

print('\nTodo listo.')