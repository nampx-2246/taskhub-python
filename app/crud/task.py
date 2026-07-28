from sqlalchemy.orm import Session, joinedload

from app.models.models import Tag, Task
from app.schemas.task import TaskCreate, TaskCreateInProject


def get_task(db: Session, task_id: int) -> Task | None:
    return db.query(Task).options(joinedload(Task.tags)).filter(Task.id == task_id).first()


def get_tasks_by_project_id(db: Session, project_id: int) -> list[Task]:
    """Get tasks of a project eager loading tags using joinedload."""
    return (
        db.query(Task)
        .options(joinedload(Task.tags))
        .filter(Task.project_id == project_id)
        .order_by(Task.id)
        .all()
    )


def create_task(db: Session, task: TaskCreate) -> Task:
    task_data = task.dict(exclude={"tag_ids"})
    db_task = Task(**task_data)
    if task.tag_ids:
        tags = db.query(Tag).filter(Tag.id.in_(task.tag_ids)).all()
        db_task.tags = tags
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def create_task_in_project(db: Session, project_id: int, task: TaskCreateInProject) -> Task:
    task_data = task.dict(exclude={"tag_ids"})
    db_task = Task(**task_data, project_id=project_id)
    if task.tag_ids:
        tags = db.query(Tag).filter(Tag.id.in_(task.tag_ids)).all()
        db_task.tags = tags
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task
