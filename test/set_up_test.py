import sys

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ..config.env_config import DATABASE_URL as SQLALCHEMY_DATABASE_URL

sys.path.append("..")


engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()
