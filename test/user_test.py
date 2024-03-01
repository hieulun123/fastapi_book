from fastapi.testclient import TestClient
from datetime import timedelta
from .. import main
from ..data.schemas import schemas
from ..router import router
# import data.schemas
from ..data.models import models
from .set_up_test import engine, override_get_db

import sys
sys.path.append("..")
models.Base.metadata.create_all(bind=engine)


main.app.dependency_overrides[router.get_db] = override_get_db

access_token_expires = timedelta(minutes=30)

client = TestClient(main.app)


test_user = schemas.UserCreate(email="hieuvt1234@example.com",
                               password="123456789")


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
