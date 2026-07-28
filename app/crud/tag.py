from sqlalchemy.orm import Session

from app.models.models import Tag
from app.schemas.tag import TagCreate


def get_tags(db: Session) -> list[Tag]:
    return db.query(Tag).order_by(Tag.id).all()


def create_tag(db: Session, tag: TagCreate) -> Tag:
    db_tag = Tag(name=tag.name)
    db.add(db_tag)
    db.commit()
    db.refresh(db_tag)
    return db_tag
