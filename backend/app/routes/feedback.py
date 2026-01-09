from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import SessionLocal
from ..models import Feedback
from ..ai.sentiment import analyze_sentiment

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/feedback")
def submit_feedback(data: dict, db: Session = Depends(get_db)):
    sentiment = analyze_sentiment(data["message"])

    feedback = Feedback(
        category=data["category"],
        message=data["message"],
        sentiment=sentiment,
        urgency=data.get("urgency", False)
    )
    db.add(feedback)
    db.commit()
    return {"status": "submitted"}
