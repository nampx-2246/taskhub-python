from sqlalchemy.orm import Session

from app.models.models import Tag


def get_tags(db: Session) -> list[Tag]:
    return db.query(Tag).order_by(Tag.id).all()
