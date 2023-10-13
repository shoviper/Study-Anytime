from fastapi import FastAPI, Request, UploadFile
from fastapi.responses import FileResponse
from pathlib import Path

from database import *
import transaction

app = FastAPI()

#== VIDEO PLAYER =====================================================================
videos_directory = Path("videos")

@app.get("/video/{course}/{filename}")
async def get_video(course: str, filename: str):
    
    video_path = videos_directory / course / filename

    if not video_path.is_file():
        return {"error": "Video not found"}

    return FileResponse(video_path, headers={"Accept-Ranges": "bytes"})

@app.post("/video/upload/{course}")
async def upload_file(course: str, file: UploadFile):
    course_directory = videos_directory / course

    if not course_directory.is_dir():
        course_directory.mkdir(parents=True)
        
    file_path = course_directory / file.filename

    if file_path.is_file():
        return {"error": "Video with the same filename already exists"}

        
    with open(file_path, "wb") as f:
        f.write(file.file.read())
    
    return {"message": "Video uploaded successfully"}

#== USER STUDENT =======================================================================
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

#== USER INSTRUCTOR =====================================================================
@app.get("/user/instructor/{id}")
async def get_student(id: str):
    
    if id == "all": 
        return root.instructor
    else:    
        return root.instructor[int(id)] if int(id) in root.instructor.keys() else {"error": "Instructor not found"}

@app.post("/user/instructor/new/{id}/{first_name}/{last_name}/{password}")
async def post_student_para(id: str, first_name: str, last_name: str, password):
    
    if int(id) in root.instructor.keys():
        return {"error": "Instructor already exists"}
    
    root.instructor[int(id)] = Instructor(int(id), first_name, last_name, password)
    transaction.commit()
    
    return {"message": "Instructor added successfully"}

#== USER OTHERS ===========================================================================
@app.get("/user/other/{username}")
async def get_student(username: str):
    
    if username == "all": 
        return root.otherUser
    else:    
        return root.otherUser[int(id)] if int(id) in root.otherUser.keys() else {"error": "OtherUser not found"}

@app.post("/user/other/new/{username}/{first_name}/{last_name}/{password}")
async def post_student_para(username: str, first_name: str, last_name: str, password):
    
    if int(username) in root.otherUser.keys():
        return {"error": "OtherUser already exists"}
    
    root.otherUser[username] = OtherUser(username, first_name, last_name, password)
    transaction.commit()
    
    return {"message": "OtherUser added successfully"}