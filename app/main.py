from typing import List

from fastapi import Depends, FastAPI, HTTPException, Response, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from . import model, schema,utils
from .database import engine, get_db

app = FastAPI()

model.Base.metadata.create_all(bind=engine)


# @app.post('/post')
# def create_post(post: Course):
#     cursor.execute("""
#         INSERT INTO course (name, instructor, duration, website) 
#         VALUES (%s, %s, %s, %s) 
#         RETURNING *
#     """, (post.name, post.instructor, post.duration, str(post.website)))
#     data = cursor.fetchone()
#     conn.commit()
#     return {"data":data}


@app.post("/course",response_model=schema.CourseReponse)
def post_courses(courses:schema.Course,db:Session=Depends(get_db)):
    new_courses = model.Course(**courses.model_dump())
    new_courses.website=str(courses.website)
    db.add(new_courses)
    db.commit()
    db.refresh(new_courses)
    return(new_courses)
    

# @app.get('/')
# def aiquest():
#     cursor.execute(""" SELECT * FROM public.course""")
#     data = cursor.fetchall()
#     return {"Data": data}

@app.get('/coursesSchemy',response_model=List[schema.CourseReponse])
def courses(db:Session = Depends(get_db)):
    course = db.query(model.Course).all()
    return course
# @app.get('/course')
# def studymart():
#     return {"django": "api"}

# @app.post("/field")
# def filed(post: Exercise):
     
#       return {"data": post}
# @app.get("/course/{id}")
# def get_course(id :int):
#     cursor.execute("""SELECT * FROM course WHERE id = %s""",(str(id),))
#     course = cursor.fetchone()
#     if not course:
#         raise HTTPException(
#             status_code = status.HTTP_404_NOT_FOUND,
#             detail= f"course with id :{id} was not found"
#         )
#     return{"course details  " :course} 
@app.get('coursesSchemy/{id}',response_model=schema.CourseReponse)
def course(id:int,db:Session=Depends(get_db)):
    course =db.query(model.Course).filter(model.Course.id==id).first()
    if not course :
        raise HTTPException(
                status_code = status.HTTP_404_NOT_FOUND,
                detail= f"course with id :{id} was not found"
                )
    return course
         
# @app.delete("/course/{id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_id(id: int):
  
#     cursor.execute("""DELETE FROM course WHERE id = %s RETURNING *""", (str(id),))
    
#     deleted_course = cursor.fetchone() 
#     conn.commit()
    
#     if deleted_course is None:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"course with id: {id} does not exist"
#         )
#     return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.delete('/courseDelete/{id}')
def course_delete(id:int,db:Session=Depends(get_db)):
    course_data= db.query(model.Course).filter(model.Course.id==id)
    course =course_data.first()
    
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Course with id {id} was not found",
        )
    course_data.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# @app.put("/course/{id}")
# def update_course(id: int,course:Course):
#     cursor.execute("""UPDATE course set name=%s,instructor=%s,duration=%s,website=%s Where id =%s RETURNING * """,(course.name,course.instructor,course.duration, str(course.website),str(id)))
    
#     update_course=cursor.fetchone()
#     conn.commit()
    
#     if update_course == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="course with id : {id} does not exit")
#     return {"data" : update_course}
    
    
    
# @app.get("/coursealechemy")
# def course(db: Session = Depends(get_db)):
#     return {"session": "sql"}


@app.put('/courseUpdate/{id}',response_model=schema.CourseReponse)
def update_course(id: int, updated_courses: schema.Course, db: Session = Depends(get_db)):
    course_query = db.query(model.Course).filter(model.Course.id == id)
    course = course_query.first()

    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")

    update_data = updated_courses.model_dump()
    update_data['website'] =str(update_data['website'])
    
    course_query.update(update_data, synchronize_session=False)
    db.commit()
    db.refresh(course)
    return  course
    
    
@app.post('/user',status_code=status.HTTP_201_CREATED)
def user_post (user:schema.User,db:Session=Depends(get_db)):
        if db.query(model.User).filter(model.User.email == user.email):
            raise HTTPException(404,detail="Email already exits")
        hashed_password = utils.hash_password(user.password)
        user.password=hashed_password
        new_user = model.User(**user.model_dump())
        
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
        
 