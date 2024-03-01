from fastapi import FastAPI, Depends

from .router.book import book_router

from .router.admin import admin_router
from .router.users import user_router
from .data.models import models
from .database import engine
from .auth import auth

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


@app.get('/')
async def Home():
    return "Welcome Home"


app.include_router(user_router.router)
app.include_router(book_router.router)
app.include_router(admin_router.router)
