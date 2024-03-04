from sqlalchemy import Column, Integer, String

from ...config.db_config import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(100), nullable=False)
    hashed_password = Column(String(255), nullable=False)
