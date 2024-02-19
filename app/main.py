from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import models, database
from app.routers import user, auth, openai

models.Base.metadata.create_all(bind=database.engine, checkfirst=True)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router)
app.include_router(auth.router)
app.include_router(openai.router)
