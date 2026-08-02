from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.deps import get_current_active_user
from app.crud.task import bookmark_task, create_task, get_task, get_tasks
from app.database import get_db
from app.models.models import User
from app.schemas.task import TaskCreate, TaskRead

router = APIRouter()


@router.post("/", response_model=TaskRead)
def create_task_endpoint(
    *,
    db: Session = Depends(get_db),
    task: TaskCreate,
    current_user: User = Depends(get_current_active_user),
):
    return create_task(db=db, task=task)


@router.get("/", response_model=list[TaskRead])
def read_tasks(
    *,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    status: str | None = None,
    priority: str | None = None,
):
    return get_tasks(db=db, skip=skip, limit=limit, status=status, priority=priority)


@router.get("/{task_id}", response_model=TaskRead)
def read_task(*, db: Session = Depends(get_db), task_id: int):
    db_task = get_task(db=db, task_id=task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task


@router.post("/{task_id}/bookmark", status_code=status.HTTP_200_OK)
def bookmark_task_endpoint(
    *,
    db: Session = Depends(get_db),
    task_id: int,
    current_user: User = Depends(get_current_active_user),
):
    db_task = bookmark_task(db=db, task_id=task_id, user=current_user)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"detail": "Task bookmarked", "task_id": task_id}
