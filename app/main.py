from fastapi import FastAPI

from . import models, database
from .routers import user, auth, openai

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

app.include_router(user.router)
app.include_router(auth.router)
app.include_router(openai.router)
