# models.py

from pydantic import BaseModel

class BookCreate(BaseModel):
    name: str
    author: str
    page_number: int

class BookResponse(BaseModel):
    id: int
    name: str
    author: str
    page_number: int


class registerCreate(BaseModel):
    email: str
    password: str
    firstName: str
    lastName: str
    country: str
    phoneNumber: str

class registerResponse(BaseModel):
    id: int
    email: str
    password: str
    firstName: str
    lastName: str
    country: str
    phoneNumber: str
