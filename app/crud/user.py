from sqlalchemy.orm import Session, joinedload

from app.core.security import hash_password
from app.models.models import User
from app.schemas.user import UserCreate, UserRegister, UserUpdate


def get_user(db: Session, user_id: int) -> User | None:
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_username(db: Session, username: str) -> User | None:
    return db.query(User).filter(User.username == username).first()


def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()


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


def create_user_with_password(db: Session, user: UserRegister | UserCreate) -> User:
    hashed_pwd = hash_password(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        hashed_password=hashed_pwd,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, db_user: User, user_update: UserUpdate) -> User:
    if user_update.full_name is not None:
        db_user.full_name = user_update.full_name
    if user_update.email is not None:
        db_user.email = user_update.email
    if user_update.password is not None and user_update.password.strip():
        db_user.hashed_password = hash_password(user_update.password)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
