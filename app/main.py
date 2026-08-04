import logging
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine
from app.models import Base
from app.routers import projects, tasks, tags, users

logger = logging.getLogger("taskhub")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

app = FastAPI(title="TaskHub API", version="0.1.0")

origins = ["*"]
if os.getenv("BACKEND_CORS_ORIGINS"):
    origins = [origin.strip() for origin in os.getenv("BACKEND_CORS_ORIGINS").split(",") if origin.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router, prefix="/api/users", tags=["users"])
app.include_router(projects.router, prefix="/api/projects", tags=["projects"])
app.include_router(tasks.router, prefix="/api/tasks", tags=["tasks"])
app.include_router(tags.router, prefix="/api/tags", tags=["tags"])


@app.on_event("startup")
def on_startup() -> None:
    """Create database tables on startup for local development."""
    logger.info("Starting TaskHub API")
    Base.metadata.create_all(bind=engine)


@app.get("/", tags=["root"])
def read_root() -> dict:
    """Root endpoint to make the API reachable at '/'."""
    return {"message": "TaskHub API running", "docs": "/docs", "openapi": "/openapi.json"}
