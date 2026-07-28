from sqlalchemy.orm import Session, joinedload
from app.models.models import User
from app.schemas.user import UserCreate


def get_user(db: Session, user_id: int) -> User | None:
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_username(db: Session, username: str) -> User | None:
    return db.query(User).filter(User.username == username).first()


def get_user_profile(db: Session, username: str) -> User | None:
    """Fetch user profile with projects and assigned tasks eager loaded using joinedload

    to prevent N+1 query problem.
    """
    return (
        db.query(User)
        .options(
            joinedload(User.projects),
            joinedload(User.tasks),
        )
        .filter(User.username == username)
        .first()
    )


def create_user(db: Session, user: UserCreate) -> User:
    db_user = User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
