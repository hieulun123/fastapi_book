from sqlalchemy.orm import Session
from ..models import user_models

from ...auth import auth

from ..schemas import user_schemas


class RecordExistedException(Exception):
    pass


class RecordNotFoundException(Exception):
    pass


class BookExistedException(Exception):
    pass


recordNotFound = RecordNotFoundException("Record not found")


def create_user(db: Session, user: user_schemas.UserCreate) -> user_models.User:
    existed = db.query(user_models.User).filter(user_models.User.email == user.email).first()
    if existed:
        msg = f"User with email {user.email} existed"
        raise RecordExistedException(msg)
    db_user = user_models.User(email=user.email,
                               hashed_password=auth.hash_password(user.password))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_with_authentication(db: Session,
                                 user: user_schemas.UserAuth) -> user_models.User:
    db_user = db.query(user_models.User).filter(user_models.User.email == user.email).first()
    if not db_user or not auth.validate_hash(user.password, db_user.hashed_password):
        raise recordNotFound
    return db_user


def get_user_by_email(db: Session, email: str) -> user_models.User:
    return db.query(user_models.User).filter(user_models.User.email == email).first()
