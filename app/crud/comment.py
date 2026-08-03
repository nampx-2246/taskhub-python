from sqlalchemy.orm import Session

from app.models.models import Comment, Task


def create_comment(db: Session, task_id: int, author_id: int, content: str) -> Comment | None:
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        return None

    comment = Comment(task_id=task_id, author_id=author_id, content=content)
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment


def get_comment(db: Session, comment_id: int) -> Comment | None:
    return db.query(Comment).filter(Comment.id == comment_id).first()


def update_comment(db: Session, comment_id: int, content: str) -> Comment | None:
    comment = get_comment(db=db, comment_id=comment_id)
    if not comment:
        return None
    comment.content = content
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment


def delete_comment(db: Session, task_id: int, comment_id: int) -> Comment | None:
    comment = db.query(Comment).filter(Comment.id == comment_id, Comment.task_id == task_id).first()
    if not comment:
        return None
    db.delete(comment)
    db.commit()
    return comment
