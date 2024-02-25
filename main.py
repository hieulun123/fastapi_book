from fastapi import FastAPI
from .router import router
from .data import models
from .data.database import engine

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


@app.get('/')
async def Home():
    return "Welcome Home"


app.include_router(router.app)
