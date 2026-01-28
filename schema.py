from pydantic import BaseModel, EmailStr #type:ignore


class ContactBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: str | None = None
    time: str | None = None
    service: str | None = None
    message: str | None = None

class ContactCreate(ContactBase):
    pass

class Contact(ContactBase):
    id: int

    class Config:
        orm_mode = True
