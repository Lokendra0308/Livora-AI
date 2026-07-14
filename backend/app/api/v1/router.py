"""
Aggregates every v1 sub-router into one `api_router`.

Why: main.py should only ever import ONE router object. As we add
auth.py, agents.py, documents.py, chat.py in later steps, we register
them here — main.py never changes again.
"""

from fastapi import APIRouter

from app.api.v1 import health

api_router = APIRouter()
api_router.include_router(health.router)
