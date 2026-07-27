from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.crud.tag import get_tags
from app.database import get_db
from app.schemas.tag import TagRead

router = APIRouter()


@router.get("/", response_model=list[TagRead])
def read_tags(*, db: Session = Depends(get_db)):
    return get_tags(db=db)
