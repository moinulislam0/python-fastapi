from pydantic import BaseModel, HttpUrl,EmailStr

class Course(BaseModel):
    name: str
    duration: float
    instructor: str
    website: HttpUrl
    
    
class CourseReponse(Course):
    id:int
    
    class config:
        orm_model=True
        
        
class User(BaseModel):
    email :EmailStr
    password: str
