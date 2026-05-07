# Notification Engine API

![Python](https://img.shields.io/badge/Python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-green)
![Cloud Run](https://img.shields.io/badge/Google_Cloud_Run-deployed-blue)
![Architecture](https://img.shields.io/badge/Architecture-Clean_Architecture-orange)

Production-ready multichannel notification system built with FastAPI and Clean Architecture.

## Live API

**Swagger UI:** https://notification-engine-247946064488.us-central1.run.app/docs

> Each user gets **2 free demo requests**. For full access contact ingenieroedissonia@gmail.com

## What It Does

Receives notification requests via REST, validates the delivery channel, and processes them through a clean layered architecture. Built to be swappable with any database or messaging provider without touching business logic.

## Architecture

```
core/                    # Domain layer
  exceptions.py          # Typed domain exceptions
  notification.py        # Notification entity (immutable dataclass)
  channel.py             # Channel entity with ChannelType enum
  repositories/          # Abstract interfaces
  services/              # NotificationService with DI
  use_cases/             # CreateNotification, GetNotification, ListChannels

infrastructure/          # Concrete implementations
  repositories/          # InMemory with thread-safe Singleton

api/                     # HTTP layer
  notification_router.py # POST /notifications
  notification_router_get.py # GET /notifications/{id}
  channel_router.py      # GET /channels
```

## Endpoints

| Method | Route | Description |
|--------|-------|-------------|
| POST | /api/v1/notifications/ | Create notification |
| GET | /api/v1/notifications/{id} | Get notification by ID |
| GET | /api/v1/channels/ | List available channels |
| GET | /health | Health check |

## Example

```bash
curl -X POST https://notification-engine-247946064488.us-central1.run.app/api/v1/notifications/ \
  -H 'Content-Type: application/json' \
  -d '{"recipient": "user@example.com", "message": "Hello", "channel": "email"}'
```

## Tech Stack

- Python 3.11+ / FastAPI 0.115 / Pydantic v2
- Clean Architecture / Dependency Injection / Singleton pattern
- Google Cloud Run / Docker / slowapi rate limiting

## Deployment

```bash
gcloud run deploy notification-engine --source . --region us-central1 --platform managed --allow-unauthenticated
```

---

**Developed by Edisson A.G.C.**
AI Engineer · Founder & CEO — M.A.I.I.E. Systems
[maiie-systems.vercel.app](https://maiie-systems.vercel.app)

Contact: ingenieroedissonia@gmail.com
