import bcrypt

from fastapi import Depends, FastAPI, HTTPException, status
from datetime import datetime, timedelta
from jose import JWTError, jwt
from ..data.schemas import UserAuth, TokenData
from typing_extensions import Annotated

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "100f98adbcdecdd265c2cdb78e94737208448948ae73dcb66b35e0cb7b813a9f"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


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


# async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         username: str = payload.get("sub")
#         if username is None:
#             raise credentials_exception
#         token_data = TokenData(username=username)
#     except JWTError:
#         raise credentials_exception
#     user = get_user(fake_users_db, username=token_data.username)
#     if user is None:
#         raise credentials_exception
#     return user


# async def get_current_active_user(
#     current_user: Annotated[User, Depends(get_current_user)]
# ):
#     if current_user.disabled:
#         raise HTTPException(status_code=400, detail="Inactive user")
#     return current_user


# async def get_current_active_admin(
#     current_admin: Annotated[User, Depends(get_current_active_user)]
# ):
#     if current_admin.role != "admin":
#         raise HTTPException(status_code=400, detail="Inactive admin")
#     return current_admin
