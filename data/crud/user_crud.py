from sqlalchemy.orm import Session
from ..models import models

from ...auth import auth

from ..schemas import schemas


class RecordExistedException(Exception):
    pass


class RecordNotFoundException(Exception):
    pass


class BookExistedException(Exception):
    pass


recordNotFound = RecordNotFoundException("Record not found")


def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    existed = db.query(models.User).filter(models.User.email == user.email).first()
    if existed:
        msg = f"User with email {user.email} existed"
        raise RecordExistedException(msg)
    db_user = models.User(email=user.email,
                          hashed_password=auth.hash_password(user.password))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_with_authentication(db: Session,
                                 user: schemas.UserAuth) -> models.User:
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if not db_user or not auth.validate_hash(user.password, db_user.hashed_password):
        raise recordNotFound
    return db_user


def get_user_by_email(db: Session, email: str) -> models.User:
    return db.query(models.User).filter(models.User.email == email).first()
