# main.py

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from api import books, register
from database import get_db, Register

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:5173",  # Assuming your SvelteKit dev server runs on this port
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



# Include API routers
app.include_router(books.router)
app.include_router(register.router)

@app.post("/login/")
async def login(email: str, password: str, db: Session = Depends(get_db)):
    user = db.query(Register).filter(Register.email == email, Register.password == password).first()
    if user:
        return {"message": "Login successful"}
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")
