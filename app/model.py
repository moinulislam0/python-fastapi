from sqlalchemy import Column, Float, Integer, String,TIMESTAMP,text

from .database import Base


class Course(Base):
    __tablename__ = "course"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    instructor = Column(String, nullable=False)
    duration = Column(Float, nullable=False)
    website = Column(String, nullable=False)
    
class User(Base):
    __tablename__ ='user'
    id=Column(Integer,nullable=False,primary_key=True)
    email = Column(String,nullable=False,unique=True)
    password= Column(String,nullable=False,)
    created_at=Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
    