import bcrypt
import os
from dotenv import load_dotenv

from fastapi import Depends, HTTPException, status
from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing_extensions import Annotated

from ..data.schemas.schemas import UserAuth, TokenData
from ..data.crud import crud
from ..database import get_db


load_dotenv()

SECRET_KEY = os.environ.get('SECRET_KEY')
ALGORITHM = os.environ.get('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = 30
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def create_access_token(user: UserAuth):
    to_encode = {"sub": user.email}
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def authorize_token(token: str):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    username: str = payload.get("sub")
    if username is None:
        raise JWTError()
    token_data = TokenData(username=username)
    return token_data


def hash_password(password: str):
    hashed = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())
    return hashed.decode('utf8')


def validate_hash(input: str, hashed: str):
    return bcrypt.checkpw(input.encode('utf8'), hashed.encode('utf8'))


async def require_authorization(token: Annotated[str, Depends(oauth2_scheme)],
                                db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": 'Bearer'}
    )
    try:
        token_data = authorize_token(token)
    except (JWTError):
        raise credentials_exception
    db_user = crud.get_user_by_email(db, token_data.username)
    if db_user is None:
        raise credentials_exception
