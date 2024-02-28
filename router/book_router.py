from typing import Annotated, Union
from datetime import date
from fastapi import Depends, APIRouter, HTTPException, Query, status
from sqlalchemy.orm import Session

from ..data import crud

from ..auth import auth

from ..data import schemas


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
               db: Session = Depends(auth.get_db)):
    filter = {
        'publish_date': publish_date,
        'author': author
    }
    books = crud.list_books(db, page=page, limit=limit, filter=filter)
    return books


@router.get("/{book_id}")
def get_book(book_id: int, db: Session = Depends(auth.get_db)):
    db_book = crud.get_book(db, book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book


@router.post("/", response_model=schemas.BookDetail)
def create_book(book: schemas.BookCreate, db: Session = Depends(auth.get_db)):
    try:
        db_book = crud.create_book(db, book)
    except crud.RecordExistedException as e:
        raise HTTPException(status_code=400, detail=str(e))
    return db_book


@router.put("/{book_id}", response_model=schemas.BookDetail)
def update_book(book_id: int, book: schemas.BookUpdate,
                db: Session = Depends(auth.get_db)):
    try:
        db_book = crud.update_book(db, book_id, book)
    except crud.RecordNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except crud.BookExistedException as e:
        raise HTTPException(status_code=400, detail=str(e))
    return db_book


@router.delete("/{book_id}")
def delete_book(book_id: int, db: Session = Depends(auth.get_db)):
    try:
        crud.delete_book(db, book_id)
    except crud.RecordNotFoundException as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {'status': 'ok'}
