from fastapi import FastAPI, Depends, HTTPException #type:ignore
from sqlalchemy.orm import Session #type:ignore
from typing import List
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware #type:ignore

from database import Base, engine, get_db
from models import ContactSubmission
from schema import ContactCreate, Contact #type:ignore

# Create tables if not exist
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Contact Form API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # <-- allow all origins
    allow_credentials=True,
    allow_methods=["*"],        # <-- allow all methods (GET, POST, etc.)
    allow_headers=["*"],        # <-- allow all headers
)

# 1️⃣ Create a new contact submission
@app.post("/contacts/", response_model=Contact)
def create_contact(contact: ContactCreate, db: Session = Depends(get_db)):
    # auto-set time if not provided
    if not contact.time:
        contact.time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    db_contact = ContactSubmission(**contact.dict())
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact

# 2️⃣ Get all contact submissions
@app.get("/contacts/", response_model=List[Contact])
def get_contacts(db: Session = Depends(get_db)):
    return db.query(ContactSubmission).all()

# 3️⃣ Get a single contact by ID
@app.get("/contacts/{contact_id}", response_model=Contact)
def get_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = db.query(ContactSubmission).filter(ContactSubmission.id == contact_id).first()
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact

# Optional: Delete a contact
@app.delete("/contacts/{contact_id}")
def delete_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = db.query(ContactSubmission).filter(ContactSubmission.id == contact_id).first()
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    db.delete(contact)
    db.commit()
    return {"message": "Contact deleted successfully"}
