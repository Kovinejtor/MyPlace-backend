from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URI = os.getenv("DATABASE_URI")

engine = create_engine(DATABASE_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Book(Base):
    __tablename__ = "book"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    author = Column(String)
    page_number = Column(Integer)

class Register(Base):
    __tablename__ = "register"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String)
    password = Column(String)
    firstName = Column(String)
    lastName = Column(String)
    country = Column(String)
    phoneNumber = Column(String)

class Place(Base):
    __tablename__ = "place"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String)
    name = Column(String)
    country = Column(String)
    city = Column(String)
    adress = Column(String)
    maxPeople = Column(Integer)
    beds = Column(Integer)
    adults = Column(Integer)
    children = Column(Integer)
    animals = Column(String)
    parking = Column(String)
    minNight = Column(Integer)
    price = Column(String)
    description = Column(String)
    folder = Column(String)
    dates = Column(String)

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
