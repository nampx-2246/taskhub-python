from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.crud.user import create_user, get_user
from app.database import get_db
from app.schemas.user import UserCreate, UserRead

router = APIRouter()


@router.post("/", response_model=UserRead)
def create_user_endpoint(*, db: Session = Depends(get_db), user: UserCreate):
    return create_user(db=db, user=user)


@router.get("/{user_id}", response_model=UserRead)
def read_user(*, db: Session = Depends(get_db), user_id: int):
    db_user = get_user(db=db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
