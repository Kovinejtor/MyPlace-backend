from pydantic import BaseModel
from typing import List

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
    gender: str
    firstName: str
    lastName: str
    country: str
    phoneNumber: str

class registerResponse(BaseModel):
    id: int
    email: str
    password: str
    gender: str
    firstName: str
    lastName: str
    country: str
    phoneNumber: str

class placeCreate(BaseModel):
    type: str
    name: str
    country: str
    city: str
    adress: str
    maxPeople: int
    beds: int
    adults: int
    children: int
    animals: str
    parking: str
    minNight: int
    description: str
    folder: str
    dates: str
    authorEmail: str

class placeResponse(BaseModel):
    id: int
    type: str
    name: str
    country: str
    city: str
    adress: str
    maxPeople: int
    beds: int
    adults: int
    children: int
    animals: str
    parking: str
    minNight: int
    description: str
    folder: str
    dates: str
    authorEmail: str