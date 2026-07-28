from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.crud.tag import create_tag, get_tags
from app.database import get_db
from app.schemas.tag import TagCreate, TagRead

router = APIRouter()


@router.get("/", response_model=list[TagRead])
def read_tags(*, db: Session = Depends(get_db)):
    return get_tags(db=db)


@router.post("/", response_model=TagRead, status_code=status.HTTP_201_CREATED)
def create_tag_endpoint(*, db: Session = Depends(get_db), tag: TagCreate):
    return create_tag(db=db, tag=tag)
