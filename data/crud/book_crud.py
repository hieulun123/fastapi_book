from sqlalchemy.orm import Session
from ..models import book_models

from ..schemas import book_schemas


class RecordExistedException(Exception):
    pass


class RecordNotFoundException(Exception):
    pass


class BookExistedException(Exception):
    pass


recordNotFound = RecordNotFoundException("Record not found")


def get_book(db: Session, book_id: int):
    return db.query(book_models.Book).filter(
        book_models.Book.id == book_id,
        book_models.Book.is_deleted == False).first()


def list_books(db: Session, page: int = 1, limit: int = 100, filter: dict = {}):
    offset = (page-1) * limit
    query = db.query(book_models.Book).filter(book_models.Book.is_deleted == False)
    for k, v in filter.items():
        if v is None:
            continue
        if k == 'publish_date':
            query = query.filter(book_models.Book.publish_date == v)
        if k == 'author':
            query = query.filter(book_models.Book.author == v.strip())

    query = query.order_by(book_models.Book.id.desc())
    return query.offset(offset).limit(limit).all()


def create_book(db: Session, book: book_schemas.BookCreate) -> book_models.Book:
    existed = db.query(book_models.Book).filter(book_models.Book.title == book.title,
                                                book_models.Book.author == book.author).first()
    if existed:
        msg = f"Book with title: {book.title}, author: {book.author} existed"
        raise RecordExistedException(msg)
    db_book = book_models.Book(title=book.title,
                               author=book.author,
                               publish_date=book.publish_date,
                               isbn=book.isbn,
                               price=book.price)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def update_book(db: Session, book_id: int,
                book: book_schemas.BookUpdate) -> book_models.Book:
    db_book = get_book(db, book_id)
    if not db_book:
        raise recordNotFound

    existed = db.query(book_models.Book).filter(book_models.Book.title == book.title,
                                                book_models.Book.author == book.author).first()
    if existed and existed.id is not book_id:
        msg = f"Cannot update, book with title: {book.title}, author: {book.author} existed"
        raise RecordExistedException(msg)
    db_book.title = book.title
    db_book.author = book.author
    db_book.publish_date = book.publish_date
    db_book.isbn = book.isbn
    db_book.price = book.price
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def delete_book(db: Session, book_id: int):
    db_book = get_book(db, book_id)
    if not db_book:
        raise recordNotFound
    db_book.is_deleted = True
    db.add(db_book)
    db.commit()
