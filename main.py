from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def aiquest():
    return {"django " :"api"}
@app.get('/course')
def studymart():
    return {"django " :"api"}