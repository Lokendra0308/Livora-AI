"""
Application entrypoint.

Responsibilities of this file ONLY:
1. Create the FastAPI app instance.
2. Wire up middleware (CORS).
3. Register the exception handlers.
4. Mount the v1 API router.

Everything else (business logic, agents, DB) lives in its own module.
Keeping main.py thin is what lets the project scale without this file
turning into a 2000-line dumping ground.
"""

import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import api_router
from app.core.config import settings
from app.core.exceptions import (
    NexusException,
    nexus_exception_handler,
    unhandled_exception_handler,
)
from app.core.logging_config import configure_logging

configure_logging()
logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.APP_NAME,
    description="Multi-Agent AI Platform — document analysis, web search, "
    "code generation, research, PDF chat, and workflow automation.",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# --- Middleware ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Exception handlers ---
app.add_exception_handler(NexusException, nexus_exception_handler)
app.add_exception_handler(Exception, unhandled_exception_handler)

# --- Routers ---
app.include_router(api_router, prefix=settings.API_V1_PREFIX)


@app.on_event("startup")
async def on_startup() -> None:
    logger.info("%s starting up in %s mode", settings.APP_NAME, settings.ENVIRONMENT)


@app.get("/")
def root() -> dict:
    return {"message": f"{settings.APP_NAME} API is running. See /docs for API documentation."}
