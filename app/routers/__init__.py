from app.routers.projects import router as projects_router
from app.routers.tasks import router as tasks_router
from app.routers.users import router as users_router

__all__ = ["projects_router", "tasks_router", "users_router"]
