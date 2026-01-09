from fastapi import FastAPI
from .routes import feedback

app = FastAPI(title="Anonymous Feedback API")

app.include_router(feedback.router)
