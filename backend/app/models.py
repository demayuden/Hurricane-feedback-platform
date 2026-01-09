from sqlalchemy import Column, Integer, Text, Boolean, Date
from .database import Base
from datetime import date

class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True, index=True)
    q1 = Column(Text)
    q2 = Column(Text)
    q3 = Column(Text)
    q4 = Column(Text)
    q5 = Column(Text)
    sentiment = Column(Text)
    urgency = Column(Boolean, default=False)
    created_date = Column(Date, default=date.today)
