from fastapi import FastAPI

from app.database import engine
from app.models import Base
from app.routers import projects, tasks, users

app = FastAPI(title="TaskHub API", version="0.1.0")
app.include_router(users.router, prefix="/api/users", tags=["users"])
app.include_router(projects.router, prefix="/api/projects", tags=["projects"])
app.include_router(tasks.router, prefix="/api/tasks", tags=["tasks"])


@app.on_event("startup")
def on_startup() -> None:
    """Create database tables on startup for local development."""
    Base.metadata.create_all(bind=engine)


@app.get("/", tags=["root"])
def read_root() -> dict:
    """Root endpoint to make the API reachable at '/'."""
    return {"message": "TaskHub API running", "docs": "/docs", "openapi": "/openapi.json"}
