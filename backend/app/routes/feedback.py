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
    combined_text = " ".join([
        data.get("q1", ""),
        data.get("q2", ""),
        data.get("q3", ""),
        data.get("q4", ""),
        data.get("q5", ""),
        data.get("q6", "")
    ])

    sentiment = analyze_sentiment(combined_text)

    feedback = Feedback(
        q1=data.get("q1"),
        q2=data.get("q2"),
        q3=data.get("q3"),
        q4=data.get("q4"),
        q5=data.get("q5"),
        q6=data.get("q6"),
        sentiment=sentiment
    )

    db.add(feedback)
    db.commit()

    return {"status": "submitted"}
