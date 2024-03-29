from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
from sqlalchemy import func

from database import get_db, Register, Book, Place
from models import BookCreate, BookResponse, registerCreate, registerResponse, placeCreate, placeResponse

from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from passlib.hash import bcrypt

app = FastAPI()

SECRET_KEY = "your-secret-key"  # Change this to a secure key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

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

@app.post("/register/", response_model=dict)
async def create_user(register: registerCreate, db: Session = Depends(get_db)):
    hashed_password = bcrypt.hash(register.password)

    db_register = Register(
        email=register.email,
        password=hashed_password,
        gender=register.gender,
        firstName=register.firstName,
        lastName=register.lastName,
        country=register.country,
        phoneNumber=register.phoneNumber
    )

    db.add(db_register)
    db.commit()
    db.refresh(db_register)

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": register.email}, expires_delta=access_token_expires)

    return {"access_token": access_token, "token_type": "bearer"}  #"user": db_register, 

@app.post("/login/")
async def login(email: str, password: str, db: Session = Depends(get_db)):
    user = db.query(Register).filter(Register.email == email).first()
    if user and bcrypt.verify(password, user.password):
        # Passwords match, create an access token
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(data={"sub": email}, expires_delta=access_token_expires)
        return {"access_token": access_token, "token_type": "bearer"}
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Invalid credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return email

@app.post("/protected-route/")
async def protected_route(current_user: str = Depends(get_current_user)):
    return current_user #email

@app.post("/addPlace/", response_model=placeResponse)
async def create_place(place: placeCreate, db: Session = Depends(get_db)):
    db_place = Place(**place.dict())
    db.add(db_place)
    db.commit()
    db.refresh(db_place)
    return db_place
    

@app.post("/books/", response_model=BookResponse)
async def create_book(book: BookCreate, db: Session = Depends(get_db)):
    db_book = Book(**book.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


@app.get("/user-info/{email}", response_model=registerResponse)
async def get_user_info(email: str, db: Session = Depends(get_db)):
    user = db.query(Register).filter(Register.email == email).first()
    if user:
        return user
    else:
        raise HTTPException(status_code=404, detail="User not found")
    
@app.delete("/delete-account/", response_model=dict)
async def delete_account(current_user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    user = db.query(Register).filter(Register.email == current_user).first()
    
    if user:
        db.delete(user)
        db.commit()

        db.query(Place).filter(Place.authorEmail == current_user).delete()
        db.commit()

        return {"message": "User and associated places deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="User not found")
    
@app.get("/count-places/", response_model=dict)
async def count_places(user_email: str, db: Session = Depends(get_db)):
    count = db.query(func.count(Place.id)).filter(Place.authorEmail == user_email).scalar()
    return {"count": count}

@app.get("/places/", response_model=List[placeResponse])
async def get_places_for_user(
    user_email: str = Query(..., title="User Email"),
    db: Session = Depends(get_db)
):
    places = db.query(Place).filter(Place.authorEmail == user_email).all()
    return places

@app.get("/places/{place_id}", response_model=placeResponse)
async def get_place(place_id: int, db: Session = Depends(get_db)):
    place = db.query(Place).filter(Place.id == place_id).first()
    if place:
        return place
    else:
        raise HTTPException(status_code=404, detail="Place not found")

@app.put("/places/{place_id}", response_model=placeResponse)
async def update_place(place_id: int, place_data: placeCreate, db: Session = Depends(get_db)):
    place = db.query(Place).filter(Place.id == place_id).first()
    if place:
        for key, value in place_data.dict().items():
            setattr(place, key, value)
        db.commit()
        db.refresh(place)
        return place
    else:
        raise HTTPException(status_code=404, detail="Place not found")