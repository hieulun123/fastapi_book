import bcrypt

from fastapi import Depends, HTTPException, status
from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing_extensions import Annotated

from ..data.schemas.user_schemas import UserAuth, TokenData
from ..data.crud import user_crud
from ..config.db_config import get_db

from ..config.env_config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES


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
    db_user = user_crud.get_user_by_email(db, token_data.username)
    if db_user is None:
        raise credentials_exception
