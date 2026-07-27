from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.crud.project import create_project, get_project, get_projects
from app.database import get_db
from app.schemas.project import ProjectCreate, ProjectRead

router = APIRouter()


@router.post("/", response_model=ProjectRead)
def create_project_endpoint(*, db: Session = Depends(get_db), project: ProjectCreate):
    return create_project(db=db, project=project)


@router.get("/", response_model=list[ProjectRead])
def read_projects(*, db: Session = Depends(get_db)):
    return get_projects(db=db)


@router.get("/{project_id}", response_model=ProjectRead)
def read_project(*, db: Session = Depends(get_db), project_id: int):
    db_project = get_project(db=db, project_id=project_id)
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")
    return db_project
