from typing import Annotated
from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from ...data.crud import user_crud

from ...auth import auth

from ...data.schemas import user_schemas

from ...config import db_config


router = APIRouter(
    tags=['auth']
)


@router.post(
    '/register',
    response_model=user_schemas.User
    )
def register(user: user_schemas.UserCreate,
             db: Session = Depends(db_config.get_db)):
    try:
        db_user = user_crud.create_user(db, user)
        return db_user
    except user_crud.RecordExistedException as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post(
    '/token',
    response_model=user_schemas.Token
    )
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                db: Session = Depends(db_config.get_db)):
    try:
        user_auth = user_schemas.UserAuth(email=form_data.username,
                                          password=form_data.password)
        user_crud.get_user_with_authentication(db, user_auth)
    except user_crud.RecordNotFoundException:
        raise HTTPException(status_code=400,
                            detail="Incorrect username or password")
    token = auth.create_access_token(user_auth)
    return {"access_token": token, "token_type": "bearer"}
