from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.types import Boolean, DECIMAL

from ...database import Base


class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    author = Column(String(100), nullable=False)
    publish_date = Column(Date, nullable=False)
    isbn = Column(String(15), nullable=False)
    price = Column(DECIMAL(2), nullable=False)
    is_deleted = Column(Boolean, default=False)
