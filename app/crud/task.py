from sqlalchemy.orm import Session, joinedload

from app.models.models import Tag, Task, User
from app.schemas.task import TaskCreate, TaskCreateInProject


def get_task(db: Session, task_id: int) -> Task | None:
    return db.query(Task).options(joinedload(Task.tags)).filter(Task.id == task_id).first()


def get_tasks(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    status: str | None = None,
    priority: str | None = None,
) -> list[Task]:
    """Get tasks with optional status and priority filters."""
    query = db.query(Task).options(joinedload(Task.tags)).order_by(Task.id)
    if status:
        query = query.filter(Task.status == status.lower())
    if priority:
        query = query.filter(Task.priority == priority.lower())
    return query.offset(skip).limit(limit).all()


def get_tasks_by_project_id(
    db: Session,
    project_id: int,
    skip: int = 0,
    limit: int = 100,
) -> list[Task]:
    """Get tasks of a project eager loading tags using joinedload."""
    return (
        db.query(Task)
        .options(joinedload(Task.tags))
        .filter(Task.project_id == project_id)
        .order_by(Task.id)
        .offset(skip)
        .limit(limit)
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


def assign_task(db: Session, task_id: int, assignee_id: int) -> Task | None:
    task = get_task(db=db, task_id=task_id)
    if not task:
        return None
    assignee = db.query(User).filter(User.id == assignee_id).first()
    if not assignee:
        return None
    with db.begin():
        task.assignee_id = assignee_id
        db.add(task)
    db.refresh(task)
    return task


def bookmark_task(db: Session, task_id: int, user) -> Task | None:
    task = get_task(db=db, task_id=task_id)
    if not task:
        return None
    if user not in task.bookmarked_by:
        task.bookmarked_by.append(user)
        db.add(task)
        db.commit()
        db.refresh(task)
    return task
