from sqlalchemy.orm import Session

from app.models.models import Project
from app.schemas.project import ProjectCreate


def get_project(db: Session, project_id: int) -> Project | None:
    return db.query(Project).filter(Project.id == project_id).first()


def create_project(db: Session, project: ProjectCreate) -> Project:
    db_project = Project(**project.dict())
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project
