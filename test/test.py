from datetime import date
from fastapi.testclient import TestClient
from datetime import timedelta
from .. import main
from ..data import schemas
from ..router import router
# import data.schemas
from ..data import models
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# from sqlalchemy.pool import StaticPool

import sys
sys.path.append("..")


SQLALCHEMY_DATABASE_URL = "postgresql://postgres:12345678@localhost/dev"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

models.Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


main.app.dependency_overrides[router.get_db] = override_get_db

access_token_expires = timedelta(minutes=30)

client = TestClient(main.app)


test_user = schemas.UserCreate(email="hieuvt1234@example.com",
                               password="123456789")
test_book = schemas.BookCreate(
    title="Harry Potter",
    author="Rowling",
    publish_date=date(year=2024, month=2, day=11),
    isbn="12345678",
    price=10.99,
)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == "Welcome Home"


def test_register():
    response = client.post(
        "/register",
        json={"email": test_user.email, "password": test_user.password},
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["email"] == "hieuvt1234@example.com"


def test_existed_email():
    response = client.post(
        "/register/",
        json={"email": test_user.email, "password": test_user.password},)
    assert response.status_code == 400
    assert response.json() == {"detail": "User with email " + test_user.email + " existed"}


def test_user_login():
    response = client.post(
        "/token",
        data={"username": test_user.email, "password": test_user.password}
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert "access_token" in data
    assert "token_type" in data


def test_create_book_with_auth():
    auth_response = client.post(
        "/token",
        data={"username": test_user.email, "password": test_user.password}
    )
    auth_data = auth_response.json()
    book_response = client.post(
        "/books",
        json={
            "title": test_book.title + 'newww',
            "author": test_book.author + 'neww',
            "publish_date": test_book.publish_date.isoformat(),
            "isbn": test_book.isbn,
            "price": test_book.price},
        headers={
            "Authorization": "Bearer {token}".format(token=auth_data['access_token']),
            "Content-Type": "application/json; charset=utf-8"
        }
    )
    assert book_response.status_code == 200
    book_data = book_response.json()
    assert "title" in book_data
    # assert book_data['title'] == test_book.title


def test_list_books():
    auth_response = client.post(
        "/token",
        data={"username": test_user.email, "password": test_user.password}
    )
    auth_data = auth_response.json()
    
    book_response = client.post(
        "/books",
        json={
            "title": test_book.title,
            "author": test_book.author,
            "publish_date": test_book.publish_date.isoformat(),
            "isbn": test_book.isbn,
            "price": test_book.price},
        headers={
            "Authorization": "Bearer {token}".format(token=auth_data['access_token']), 
            "Content-Type": "application/json; charset=utf-8"
        }
    )
    book = book_response.json()

    list_response = client.get("/books")
    booklist = list_response.json()
    assert list_response.status_code == 200
    assert (len(booklist)) > 0

    # detail_response = client.get("/books/{id}".format(id=1))
    # book_1 = detail_response.json()
    # assert detail_response.status_code == 200
    # assert book_1['id'] == book['id']
