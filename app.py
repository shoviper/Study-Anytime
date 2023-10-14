from fastapi import FastAPI, Request, UploadFile, HTTPException
from fastapi.responses import FileResponse
from pathlib import Path

from database import *
import transaction

app = FastAPI()

# == VIDEO PLAYER =====================================================================
videos_directory = Path("videos")

@app.get("/video/{course_id}/{filename}")
async def get_video(course_id: int, filename: str):
    video_path = videos_directory / str(course_id) / filename

    if not course_id in root.course.keys():
        raise HTTPException(404, detail="db_error: Course not found")

    if not root.course[course_id].isIn(Video(filename)):
        raise HTTPException(404, detail="db_error: Video not found")

    if not video_path.is_file():
        raise HTTPException(404, detail="fs_error: Video not found")

    return FileResponse(video_path, headers={"Accept-Ranges": "bytes"})

@app.post("/video/upload/{course_id}/{instructor_id}")
async def upload_file(course_id: int, instructor_id: int, file: UploadFile):
    course_directory = videos_directory / str(course_id)

    if not instructor_id in root.instructor.keys():
        raise HTTPException(404, detail="db_error: Instructor not found")

    file_path = course_directory / file.filename

    if root.course[course_id].isIn(Video(file.filename)):
        raise HTTPException(404, detail="db_error: Video with the same filename already exists")

    if file_path.is_file():
        raise HTTPException(404, detail="fs_error: Video with the same filename already exists")

    with open(file_path, "wb") as f:
        f.write(file.file.read())

    root.course[course_id].addVideo(file.filename)
    transaction.commit()

    return {"message": "Video uploaded successfully"}


# == USER STUDENT =======================================================================
@app.get("/user/student/{id}")
async def get_student(id: int):
    if id == "all":
        return root.student
    else:
        id = int(id)
        return root.student[id] if id in root.student.keys() else {"error": "Student not found"}

@app.post("/user/student/new/{id}/{first_name}/{last_name}/{password}")
async def post_student(id: int, first_name: str, last_name: str, password):
    if int(id) in root.student.keys():
        raise HTTPException(404, detail="db_error: Student already exists")

    root.student[id] = Student(id, first_name, last_name, password)
    transaction.commit()

    return {"message": "Student added successfully"}


# == USER INSTRUCTOR =====================================================================
@app.get("/user/instructor/{id}")
async def get_instructor(id: str):
    if id == "all":
        return root.instructor
    else:
        id = int(id)
        return root.instructor[id] if id in root.instructor.keys() else {"error": "Instructor not found"}

@app.post("/user/instructor/new/{id}/{first_name}/{last_name}/{password}")
async def post_instructor(id: int, first_name: str, last_name: str, password: str):
    if int(id) in root.instructor.keys():
        raise HTTPException(404, detail="db_error: Instructor already exists")

    root.instructor[id] = Instructor(id, first_name, last_name, password)
    transaction.commit()

    return {"message": "Instructor added successfully"}

# == USER OTHERS ===========================================================================
@app.get("/user/other/{username}")
async def get_other(username: str):
    if username == "all":
        return root.otherUser
    else:
        return (
            root.otherUser[username]
            if username in root.otherUser.keys()
            else {"error": "OtherUser not found"}
        )

@app.post("/user/other/new/{username}/{first_name}/{last_name}/{password}")
async def post_other(username: str, first_name: str, last_name: str, password: str):
    if username in root.otherUser.keys():
        raise HTTPException(404, detail="OtherUser: Instructor already exists")

    root.otherUser[username] = OtherUser(username, first_name, last_name, password)
    transaction.commit()

    return {"message": "OtherUser added successfully"}


# == COURSE ===========================================================================
@app.get("/course/{course_id}")
async def get_course(course_id: str):
    if course_id == "all":
        return root.course
    else:
        return root.course[int(course_id)] if int(course_id) in root.course.keys() else {"error": "Course not found"}
        

@app.post("/course/new/{course_id}/{name}/{instructor_id}/{public}")
async def post_course(course_id: str, name: str, instructor_id: str, public: bool):
    if int(course_id) in root.course.keys():
        raise HTTPException(404, detail="db_error: Course already exists")

    if not int(instructor_id) in root.instructor.keys():
        raise HTTPException(404, detail="db_error: Instructor not found")
    
    course_directory = videos_directory / course_id
    course_directory.mkdir(parents=True)
    
    root.course[int(course_id)] = Course(int(course_id), name, instructor_id, public)
    root.instructor[int(instructor_id)].addCourse(int(course_id))
    transaction.commit()

    return {"message": "Course added successfully"}

transaction.commit()