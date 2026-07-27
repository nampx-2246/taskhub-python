from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.crud.task import create_task, get_task
from app.database import get_db
from app.schemas.task import TaskCreate, TaskRead

router = APIRouter()


@router.post("/", response_model=TaskRead)
def create_task_endpoint(*, db: Session = Depends(get_db), task: TaskCreate):
    return create_task(db=db, task=task)


@router.get("/{task_id}", response_model=TaskRead)
def read_task(*, db: Session = Depends(get_db), task_id: int):
    db_task = get_task(db=db, task_id=task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task
