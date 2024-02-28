from typing import Annotated, Union
from fastapi import Depends, APIRouter, HTTPException, Query, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from ..data import crud

from ..auth import auth

from ..data import schemas


router = APIRouter()


@router.post('/register', response_model=schemas.User, tags=['auth'])
def register(user: schemas.UserCreate, db: Session = Depends(auth.get_db)):
    try:
        db_user = crud.create_user(db, user)
        return db_user
    except crud.RecordExistedException as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post('/token', response_model=schemas.Token, tags=['auth'])
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                db: Session = Depends(auth.get_db)):
    try:
        user_auth = schemas.UserAuth(email=form_data.username,
                                     password=form_data.password)
        crud.get_user_with_authentication(db, user_auth)
    except crud.RecordNotFoundException:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    token = auth.create_access_token(user_auth)
    return {"access_token": token, "token_type": "bearer"}
