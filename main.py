from fastapi import FastAPI, Depends
from .router import book_router, user_router, admin_router
from .data import models
from .data.database import engine
from .auth import auth

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


@app.get('/')
async def Home():
    return "Welcome Home"


app.include_router(user_router.router)
app.include_router(book_router.router)
app.include_router(admin_router.router)
