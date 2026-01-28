from sqlalchemy import Column, Integer, String, Text #type:ignore
from database import Base

class ContactSubmission(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False)
    phone = Column(String(20), nullable=True)
    time = Column(String(20), nullable=True)
    message = Column(Text, nullable=True)
    service = Column(String(100), nullable=True)
