"""
Health check endpoint.

Why it exists on day one: Render/Docker/uptime monitors and the frontend
need a cheap, dependency-free endpoint to confirm the API process is
alive before we've built anything else. It also becomes the template
for every other router we add in later steps.
"""

from fastapi import APIRouter

from app.core.config import settings

router = APIRouter(tags=["health"])


@router.get("/health")
def health_check() -> dict:
    return {
        "status": "ok",
        "app": settings.APP_NAME,
        "environment": settings.ENVIRONMENT,
    }
