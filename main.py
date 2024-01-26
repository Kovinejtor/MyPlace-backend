from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

from database import get_db, Register, Book, Place
from models import BookCreate, BookResponse, registerCreate, registerResponse, placeCreate, placeResponse

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:5173", 
    "http://127.0.0.1",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/register/", response_model=registerResponse)
async def create_user(register: registerCreate, db: Session = Depends(get_db)):
    db_register = Register(**register.dict())
    db.add(db_register)
    db.commit()
    db.refresh(db_register)
    return db_register

@app.post("/login/")
async def login(email: str, password: str, db: Session = Depends(get_db)):
    user = db.query(Register).filter(Register.email == email, Register.password == password).first()
    if user:
        return {"message": "Login successful"}
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
@app.post("/addPlace/", response_model=placeResponse)
async def create_place(
    place: placeCreate, 
    files: List[UploadFile] = File(...), 
    db: Session = Depends(get_db)
):
    try:
        print("Received Place data:", place.dict())
        print("Received Files:", files)

        # Save place details to the database
        db_place = Place(**place.dict())
        db.add(db_place)
        db.commit()
        db.refresh(db_place)

        # Save image URLs to the database
        image_urls = []
        for file in files:
            # Process and save the file, and get its URL
            # For simplicity, you can store the URLs directly. In production, consider using a dedicated storage service.
            image_url = f"/path/to/your/image/{file.filename}"
            image_urls.append(image_url)

        db_place.images = image_urls
        db.commit()
        db.refresh(db_place)

        return db_place
    except Exception as e:
        print("Error:", e)
        # Log the error details to a file or another logging mechanism
        with open('error.log', 'a') as log_file:
            log_file.write(str(e) + '\n')
        raise HTTPException(status_code=422, detail=str(e))

@app.post("/books/", response_model=BookResponse)
async def create_book(book: BookCreate, db: Session = Depends(get_db)):
    db_book = Book(**book.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book
