from fastapi import FastAPI, Request, UploadFile, HTTPException
from fastapi.responses import FileResponse
from pathlib import Path

from database import *
import transaction

app = FastAPI()

# == VIDEO PLAYER =====================================================================
videos_directory = Path("videos")

@app.get("/video/{id}/{filename}")
async def get_video(id: str, filename: str):
    video_path = videos_directory / id / filename

    if not int(id) in root.course.keys():
        raise HTTPException(404, detail="db_error: Course not found")

    if not root.course[int(id)].isIn(Video(filename)):
        raise HTTPException(404, detail="db_error: Video not found")

    if not video_path.is_file():
        raise HTTPException(404, detail="fs_error: Video not found")

    return FileResponse(video_path, headers={"Accept-Ranges": "bytes"})

@app.post("/video/upload/{id}")
async def upload_file(id: str, file: UploadFile):
    course_directory = videos_directory / id

    if not course_directory.is_dir():
        course_directory.mkdir(parents=True)

    if not int(id) in root.course.keys():
        root.course[int(id)] = Course(int(id), "aaa", "bbb", True)

    file_path = course_directory / file.filename

    if root.course[int(id)].isIn(Video(file.filename)):
        raise HTTPException(
            404, detail="db_error: Video with the same filename already exists"
        )

    if file_path.is_file():
        raise HTTPException(
            404, detail="fs_error: Video with the same filename already exists"
        )

    with open(file_path, "wb") as f:
        f.write(file.file.read())

    root.course[int(id)].addVideo(Video(file.filename))
    transaction.commit()
    return {"message": "Video uploaded successfully"}


# == USER STUDENT =======================================================================
@app.get("/user/student/{id}")
async def get_student(id: str):
    if id == "all":
        return root.student
    else:
        return root.student[int(id)] if int(id) in root.student.keys() else {"error": "Student not found"}
        

@app.post("/user/student/new/{id}/{first_name}/{last_name}/{password}")
async def post_student(id: str, first_name: str, last_name: str, password):
    if int(id) in root.student.keys():
        raise HTTPException(404, detail="db_error: Student already exists")

    root.student[int(id)] = Student(int(id), first_name, last_name, password)
    transaction.commit()

    return {"message": "Student added successfully"}


# == USER INSTRUCTOR =====================================================================
@app.get("/user/instructor/{id}")
async def get_instructor(id: str):
    if id == "all":
        return root.instructor
    else:
        return root.instructor[int(id)] if int(id) in root.instructor.keys() else {"error": "Instructor not found"}

@app.post("/user/instructor/new/{id}/{first_name}/{last_name}/{password}")
async def post_instructor(id: str, first_name: str, last_name: str, password):
    if int(id) in root.instructor.keys():
        raise HTTPException(404, detail="db_error: Instructor already exists")

    root.instructor[int(id)] = Instructor(int(id), first_name, last_name, password)
    transaction.commit()

    return {"message": "Instructor added successfully"}

@app.post("/user/instructor/new/{id}/{first_name}/{last_name}/{password}")
async def post_student_para(id: str, first_name: str, last_name: str, password):
    if int(id) in root.instructor.keys():
        raise HTTPException(404, detail="db_error: Instructor already exists")

    root.instructor[int(id)] = Instructor(int(id), first_name, last_name, password)
    transaction.commit()

    return {"message": "Instructor added successfully"}

# == USER OTHERS ===========================================================================
@app.get("/user/other/{username}")
async def get_other(username: str):
    if username == "all":
        return root.otherUser
    else:
        return (
            root.otherUser[int(id)]
            if int(id) in root.otherUser.keys()
            else {"error": "OtherUser not found"}
        )

@app.post("/user/other/new/{username}/{first_name}/{last_name}/{password}")
async def post_other(username: str, first_name: str, last_name: str, password):
    if int(username) in root.otherUser.keys():
        raise HTTPException(404, detail="OtherUser: Instructor already exists")

    root.otherUser[username] = OtherUser(username, first_name, last_name, password)
    transaction.commit()

    return {"message": "OtherUser added successfully"}
