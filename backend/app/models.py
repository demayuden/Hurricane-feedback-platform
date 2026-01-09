from sqlalchemy import Column, Integer, Text, Boolean, Date
from .database import Base

class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True, index=True)
    category = Column(Text)
    message = Column(Text)
    sentiment = Column(Text)
    topic = Column(Text)
    urgency = Column(Boolean, default=False)
    created_date = Column(Date)
