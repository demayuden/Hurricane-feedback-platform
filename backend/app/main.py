from fastapi import FastAPI
from .routes import feedback
from .database import Base, engine
from . import models

app = FastAPI(title="Anonymous Feedback API")

# CREATE TABLES AUTOMATICALLY
Base.metadata.create_all(bind=engine)

app.include_router(feedback.router)
