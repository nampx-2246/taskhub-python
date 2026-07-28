from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.crud.project import create_project, get_project, get_project_with_tasks, get_projects
from app.crud.task import create_task_in_project, get_tasks_by_project_id
from app.database import get_db
from app.schemas.project import ProjectCreate, ProjectRead, ProjectWithTasksRead
from app.schemas.task import TaskCreateInProject, TaskRead

router = APIRouter()


@router.post("/", response_model=ProjectRead, status_code=status.HTTP_201_CREATED)
def create_project_endpoint(*, db: Session = Depends(get_db), project: ProjectCreate):
    return create_project(db=db, project=project)


@router.get("/", response_model=list[ProjectRead])
def read_projects(*, db: Session = Depends(get_db)):
    return get_projects(db=db)


@router.get("/{project_id}", response_model=ProjectWithTasksRead)
def read_project(*, db: Session = Depends(get_db), project_id: int):
    db_project = get_project_with_tasks(db=db, project_id=project_id)
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")
    return db_project


@router.get("/{project_id}/tasks", response_model=list[TaskRead])
def read_project_tasks(*, db: Session = Depends(get_db), project_id: int):
    """GET /api/projects/{project_id}/tasks

    Get all tasks belonging to a specific project.
    """
    db_project = get_project(db=db, project_id=project_id)
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")
    return get_tasks_by_project_id(db=db, project_id=project_id)


@router.post("/{project_id}/tasks", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
def create_task_for_project(
    *, db: Session = Depends(get_db), project_id: int, task: TaskCreateInProject
):
    """POST /api/projects/{project_id}/tasks

    Create a new task directly inside a specific project.
    """
    db_project = get_project(db=db, project_id=project_id)
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")
    return create_task_in_project(db=db, project_id=project_id, task=task)
