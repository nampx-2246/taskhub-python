from sqlalchemy.orm import Session, joinedload

from app.models.models import Project, Task
from app.schemas.project import ProjectCreate


def get_project(db: Session, project_id: int) -> Project | None:
    return db.query(Project).filter(Project.id == project_id).first()


def get_project_with_tasks(db: Session, project_id: int) -> Project | None:
    """Fetch project with all tasks eager loaded using joinedload."""
    return (
        db.query(Project)
        .options(joinedload(Project.tasks).joinedload(Task.tags))
        .filter(Project.id == project_id)
        .first()
    )


def get_projects(db: Session) -> list[Project]:
    return db.query(Project).order_by(Project.id).all()


def create_project(db: Session, project: ProjectCreate) -> Project:
    db_project = Project(**project.dict())
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project
