from fastapi import FastAPI, HTTPException, status, Response, Depends
from pydantic import BaseModel, HttpUrl
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import model
from sqlalchemy.orm import Session
from .database import engine, get_db

app = FastAPI()

model.Base.metadata.create_all(bind=engine)

class Course(BaseModel):
    name: str
    duration: float
    instructor: str
    website: HttpUrl

class Exercise(BaseModel): 
    name: str
    field_name: str

while True:
    try:
        conn = psycopg2.connect(
            host='localhost', database='postgres', user='postgres', 
            password='1234', cursor_factory=RealDictCursor
        )   
        cursor = conn.cursor() 
        print('successfully connected database')
        break
    except Exception as error:
        print("Database connection failed ")
        print("error", error)
        time.sleep(2)


@app.post('/post')
def create_post(post: Course):
    cursor.execute("""
        INSERT INTO course (name, instructor, duration, website) 
        VALUES (%s, %s, %s, %s) 
        RETURNING *
    """, (post.name, post.instructor, post.duration, str(post.website)))
    data = cursor.fetchone()
    conn.commit()
    return {"data":data}


@app.post("/course")
def post_courses(courses:Course,db:Session=Depends(get_db)):
    new_courses = model.Course(
       name=courses.name,
      insturctor=courses.instructor,
       duration= courses.duration,
       website =str(courses.website)
    )
    db.add(new_courses)
    db.commit()
    db.refresh(new_courses)
    return("Courese ", new_courses)
    

@app.get('/')
def aiquest():
    cursor.execute(""" SELECT * FROM public.course""")
    data = cursor.fetchall()
    return {"Data": data}

@app.get('/course')
def studymart():
    return {"django": "api"}

@app.post("/field")
def filed(post: Exercise):
     
      return {"data": post}
@app.get("/course/{id}")
def get_course(id :int):
    cursor.execute("""SELECT * FROM course WHERE id = %s""",(str(id),))
    course = cursor.fetchone()
    if not course:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail= f"course with id :{id} was not found"
        )
    return{"course details  " :course}   
@app.delete("/course/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_id(id: int):
  
    cursor.execute("""DELETE FROM course WHERE id = %s RETURNING *""", (str(id),))
    
    deleted_course = cursor.fetchone() 
    conn.commit()
    
    if deleted_course is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"course with id: {id} does not exist"
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/course/{id}")
def update_course(id: int,course:Course):
    cursor.execute("""UPDATE course set name=%s,instructor=%s,duration=%s,website=%s Where id =%s RETURNING * """,(course.name,course.instructor,course.duration, str(course.website),str(id)))
    
    update_course=cursor.fetchone()
    conn.commit()
    
    if update_course == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="course with id : {id} does not exit")
    return {"data" : update_course}
    
    
    
@app.get("/coursealechemy")
def course(db: Session = Depends(get_db)):
    return {"session": "sql"}