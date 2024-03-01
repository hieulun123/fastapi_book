from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import sys
import os
from dotenv import load_dotenv

sys.path.append("..")

load_dotenv()
SQLALCHEMY_DATABASE_URL = os.environ.get('DATABASE_URL')

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()
