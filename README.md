# Notification Engine API

Sistema de notificaciones multicanal production-ready generado autonomamente por **M.A.I.I.E. Systems**.

## Arquitectura

```
core/           # Dominio puro -- entidades, excepciones, use cases, interfaces
infrastructure/ # Repositorios InMemory con Singleton thread-safe
api/            # Endpoints FastAPI con inyeccion de dependencias
```

## Stack

- Python 3.12+
- FastAPI 0.115
- Pydantic v2
- Clean Architecture
- Singleton thread-safe

## Endpoints

| Metodo | Ruta | Descripcion |
|--------|------|-------------|
| GET | /api/v1/notifications/{id} | Obtener notificacion por ID |
| POST | /api/v1/notifications | Crear notificacion |
| GET | /api/v1/channels | Listar canales disponibles |

## Swagger

Documentacion interactiva en `/docs` al correr el servidor.

## Instalacion

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

## Generado por M.A.I.I.E.

Pipeline: ARCHITECT (gemini-2.5-flash-lite) -> ENGINEER (gemini-2.5-pro) -> AUDITOR (gemini-2.5-pro)

Cada archivo validado con contratos arquitectonicos formales y aprobado 100% por el AUDITOR.

---

Built with M.A.I.I.E. Systems by Edisson A.G.C.