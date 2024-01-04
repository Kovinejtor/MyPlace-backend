# api/books.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db, Register
from models import registerCreate, registerResponse

router = APIRouter()

@router.post("/register/", response_model=registerResponse)
async def create_user(register: registerCreate, db: Session = Depends(get_db)):
    db_register = Register(**register.dict())
    db.add(db_register)
    db.commit()
    db.refresh(db_register)
    return db_register