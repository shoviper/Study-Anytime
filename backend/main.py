from fastapi import FastAPI, Request, Depends, UploadFile, HTTPException
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from database import *
from auth.auth_handler import *
from auth.auth_bearer import JWTBearer

import transaction
import logging

app = FastAPI()
templates = Jinja2Templates(directory="backend/templates")
logging.basicConfig(level=logging.DEBUG)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.on_event("shutdown")
async def shutdown():
    transaction.commit()
    db.close()

# == connect to login page =====================================================================
@app.get("/login", response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

# == connect to sign up page =====================================================================
@app.get("/signup", response_class=HTMLResponse)
async def signup(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})

# == connect to resetpassword page =====================================================================
@app.get("/resetpassword", response_class=HTMLResponse)
async def resetpassword(request: Request):
    return templates.TemplateResponse("resetpassword.html", {"request": request})


# == VIDEO PLAYER =====================================================================
videos_directory = Path("db/course_videos")

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

    temp_course = Course(root.course[course_id].id, root.course[course_id].name, root.course[course_id].instructor, root.course[course_id].public)
    for c in root.course[course_id].videos:
        temp_course.addVideo(c)
    temp_course.addVideo(file.filename)
    root.course[course_id] = temp_course
    
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

@app.get("/user/signIn/student/{id}/{password}")
async def signIn_student(id: int, password: str):
    if check_user(root.student, id, password):
        return signJWT(id)
    return {"error": "Wrong login details!"}
    
@app.post("/user/signUp/student/{id}/{first_name}/{last_name}/{password}")
async def signUp_student(id: int, first_name: str, last_name: str, password):
    if int(id) in root.student.keys():
        raise HTTPException(404, detail="db_error: Student already exists")

    root.student[id] = Student(id, first_name, last_name, password)
    transaction.commit()

    return signJWT(id)

# == USER INSTRUCTOR =====================================================================
@app.get("/user/instructor/{id}")
async def get_instructor(id: str):
    if id == "all":
        return root.instructor
    else:
        id = int(id)
        return root.instructor[id] if id in root.instructor.keys() else {"error": "Instructor not found"}

@app.get("/user/signIn/instructor/{id}/{password}")
async def signIn_instructor(id: int, password: str):
    if check_user(root.instructor, id, password):
        return signJWT(id)
    return {"error": "Wrong login details!"}
    
@app.post("/user/signUp/instructor/{id}/{first_name}/{last_name}/{password}")
async def signUp_instructor(id: int, first_name: str, last_name: str, password: str):
    if int(id) in root.instructor.keys():
        raise HTTPException(404, detail="db_error: Instructor already exists")

    root.instructor[id] = Instructor(id, first_name, last_name, password)
    transaction.commit()

    return signJWT(id)
        
# == USER OTHERS ===========================================================================
@app.get("/user/other/{username}")
async def get_other(username: str):
    if username == "all":
        return root.otherUser
    else:
        return root.otherUser[username] if username in root.otherUser.keys() else {"error": "OtherUser not found"}

@app.get("/user/signIn/other/{id}/{password}")
async def signIn_other(id: int, password: str):
    if check_user(root.otherUser, id, password):      
        return signJWT(id)
    return {"error": "Wrong login details!"}

@app.post("/user/signUp/other/{username}/{first_name}/{last_name}/{password}")
async def signUp_other(username: str, first_name: str, last_name: str, password: str):
    if username in root.otherUser.keys():
        raise HTTPException(404, detail="OtherUser: Instructor already exists")

    root.otherUser[username] = OtherUser(username, first_name, last_name, password)
    transaction.commit()

    return signJWT(id)


# == COURSE ===========================================================================
@app.get("/course/{course_id}")
async def get_course(course_id: str):
    if course_id == "all":
        return root.course
    else:
        return root.course[int(course_id)] if int(course_id) in root.course.keys() else {"error": "Course not found"}

@app.post("/course/new/{course_id}/{name}/{instructor_id}/{public}", dependencies=[Depends(JWTBearer())])
async def post_course(course_id: str, name: str, instructor_id: str, public: bool):
    if int(course_id) in root.course.keys():
        raise HTTPException(404, detail="db_error: Course already exists")

    if not int(instructor_id) in root.instructor.keys():
        raise HTTPException(404, detail="db_error: Instructor not found")
    
    course_directory = videos_directory / course_id
    course_directory.mkdir(parents=True)
    
    root.course[int(course_id)] = Course(int(course_id), name, instructor_id, public)
    
    temp_instructor = Instructor(int(instructor_id), root.instructor[int(instructor_id)].first_name, root.instructor[int(instructor_id)].last_name, root.instructor[int(instructor_id)].password)
    for c in root.instructor[int(instructor_id)].courses:
        temp_instructor.addCourse(c)
    temp_instructor.addCourse(int(course_id))
    root.instructor[int(instructor_id)] = temp_instructor
    
    transaction.commit()

    return {"message": "Course added successfully"}
