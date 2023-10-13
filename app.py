from fastapi import FastAPI, Request, UploadFile
from fastapi.responses import FileResponse
from pathlib import Path

app = FastAPI()
directory = Path("video_files")

@app.get("/videos/{video_filename}")
async def get_video(video_filename: str):
    
    video_path = directory / video_filename

    if not video_path.is_file():
        return {"error": "Video not found"}

    return FileResponse(video_path, headers={"Accept-Ranges": "bytes"})

@app.post("/upload/")
async def upload_file(file: UploadFile):
    
    with open(f"{directory}/{file.filename}", "wb") as f:
        f.write(file.file.read())


from database import *
import transaction

@app.get("/user/student/{id}")
async def get_student(id: str):
    
    if id == "all": 
        return root.student
    else:    
        return root.student[int(id)] if int(id) in root.student.keys() else {"error": "Student not found"}

@app.post("/user/student/new/{id}/{first_name}/{last_name}/{password}")
async def post_student_para(id: str, first_name: str, last_name: str, password):
    
    if int(id) in root.student.keys():
        return {"error": "Student already exists"}
    
    root.student[int(id)] = Student(int(id), first_name, last_name, password)
    transaction.commit()
    
    return {"message": "Student added successfully"}
