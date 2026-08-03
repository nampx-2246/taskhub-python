from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.deps import get_current_active_user, verify_project_manager
from app.crud.comment import create_comment, delete_comment, get_comment, update_comment
from app.crud.task import assign_task, bookmark_task, create_task, get_task, get_tasks
from app.database import get_db
from app.models.models import User
from app.schemas.comment import CommentCreate, CommentRead, CommentUpdate
from app.schemas.task import TaskAssign, TaskCreate, TaskRead

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


@router.post("/{task_id}/assign", response_model=TaskRead)
def assign_task_endpoint(
    *,
    db: Session = Depends(get_db),
    task_id: int,
    task_assign: TaskAssign,
    current_user: User = Depends(verify_project_manager),
):
    db_task = assign_task(db=db, task_id=task_id, assignee_id=task_assign.assignee_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found or assignee invalid")
    return db_task


@router.post("/{task_id}/comments", response_model=CommentRead, status_code=status.HTTP_201_CREATED)
def create_task_comment(
    *,
    db: Session = Depends(get_db),
    task_id: int,
    comment_in: CommentCreate,
    current_user: User = Depends(get_current_active_user),
):
    db_comment = create_comment(
        db=db,
        task_id=task_id,
        author_id=current_user.id,
        content=comment_in.content,
    )
    if not db_comment:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_comment


@router.put("/{task_id}/comments/{comment_id}", response_model=CommentRead)
def update_task_comment(
    *,
    db: Session = Depends(get_db),
    task_id: int,
    comment_id: int,
    comment_in: CommentUpdate,
    current_user: User = Depends(get_current_active_user),
):
    db_comment = get_comment(db=db, comment_id=comment_id)
    if not db_comment or db_comment.task_id != task_id:
        raise HTTPException(status_code=404, detail="Comment not found")

    is_owner = db_comment.author_id == current_user.id
    if not is_owner and current_user.role not in {"admin", "project_manager"}:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only comment owner, admin, or project manager can update this comment",
        )

    updated_comment = update_comment(db=db, comment_id=comment_id, content=comment_in.content)
    if not updated_comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    return updated_comment


@router.delete("/{task_id}/comments/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task_comment(
    *,
    db: Session = Depends(get_db),
    task_id: int,
    comment_id: int,
    current_user: User = Depends(get_current_active_user),
):
    db_comment = get_comment(db=db, comment_id=comment_id)
    if not db_comment or db_comment.task_id != task_id:
        raise HTTPException(status_code=404, detail="Comment not found")

    is_owner = db_comment.author_id == current_user.id
    if not is_owner and current_user.role not in {"admin", "project_manager"}:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only comment owner, admin, or project manager can delete this comment",
        )

    deleted = delete_comment(db=db, task_id=task_id, comment_id=comment_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Comment not found")
    return None


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
