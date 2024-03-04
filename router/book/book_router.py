from typing import Union
from datetime import date
from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session

from ...config import db_config

from ...data.crud import book_crud

from ...auth import auth

from ...data.schemas import book_schemas


router = APIRouter(
    prefix="/books",
    tags=["books"],
    dependencies=[Depends(auth.require_authorization)],
    responses={404: {"description": "Not found"}}
)


@router.get("/")
def list_books(page: int = 1,
               limit: int = 100,
               publish_date: Union[date, None] = None,
               author: Union[str, None] = None,
               db: Session = Depends(db_config.get_db)):
    filter = {
        'publish_date': publish_date,
        'author': author
    }
    books = book_crud.list_books(db, page=page, limit=limit, filter=filter)
    return books


@router.get("/{book_id}")
def get_book(book_id: int,
             db: Session = Depends(db_config.get_db)):
    db_book = book_crud.get_book(db, book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book


@router.post("/", response_model=book_schemas.BookDetail)
def create_book(book: book_schemas.BookCreate,
                db: Session = Depends(db_config.get_db)):
    try:
        db_book = book_crud.create_book(db, book)
    except book_crud.RecordExistedException as e:
        raise HTTPException(status_code=400, detail=str(e))
    return db_book


@router.put("/{book_id}", response_model=book_schemas.BookDetail)
def update_book(book_id: int, book: book_schemas.BookUpdate,
                db: Session = Depends(db_config.get_db)):
    try:
        db_book = book_crud.update_book(db, book_id, book)
    except book_crud.RecordNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except book_crud.BookExistedException as e:
        raise HTTPException(status_code=400, detail=str(e))
    return db_book


@router.delete("/{book_id}")
def delete_book(book_id: int, db: Session = Depends(db_config.get_db)):
    try:
        book_crud.delete_book(db, book_id)
    except book_crud.RecordNotFoundException as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {'status': 'ok'}
