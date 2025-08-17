from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import models
from utils import generate_code

MAX_RETRIES = 5

def create_short_url(db: Session, original_url: str) -> models.UrlMap:
    for _ in range(MAX_RETRIES):
        code = generate_code(6)
        entry = models.UrlMap(code=code, original_url=original_url)
        db.add(entry)
        try:
            db.commit()
            db.refresh(entry)
            return entry
        except IntegrityError:
            db.rollback()
            continue
    raise RuntimeError("Could not generate unique code after retries")


def get_by_code(db: Session, code: str) -> models.UrlMap | None:
    return db.query(models.UrlMap).filter(models.UrlMap.code == code).first()


def increment_click(db: Session, entry: models.UrlMap) -> None:
    entry.click_count = (entry.click_count or 0) + 1
    db.add(entry)
    db.commit()