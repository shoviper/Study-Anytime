
from math import exp
from fastapi import FastAPI, Request, Response, Depends, UploadFile, HTTPException, Cookie, Form
from fastapi.responses import FileResponse, HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from database import *
from auth.auth_handler import *
from auth.auth_bearer import JWTBearer

import transaction
import logging

app = FastAPI()
templates = Jinja2Templates(directory="templates")
logging.basicConfig(level=logging.DEBUG)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request, access_token: str = Cookie(None)):
    try:
        token = decodeJWT(access_token)
        id = token["id"]
        role = token["role"]
        username = f"{get_user(id).first_name} {get_user(id).last_name}"
        return templates.TemplateResponse("index.html", {"request": request, "username": username, "role": role})
    except:
        return templates.TemplateResponse("index.html", {"request": request})
        
    
@app.on_event("shutdown")
async def shutdown():
    transaction.commit()
    db.close()

# == connect to main page ============================================================
@app.get("/main", response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "invalid": False})

# == connect to login page ============================================================
@app.get("/login", response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request, "invalid": False})

# == connect to mainpage page ============================================================
@app.get("/mainpage", response_class=HTMLResponse)
async def mainpage(request: Request):
    return templates.TemplateResponse("mainpage.html", {"request": request, "invalid": False})

# == connect to sign up page ==========================================================
@app.get("/signup", response_class=HTMLResponse)
async def signup(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})

@app.post("/signup")
async def signupp(data: dict):
    return data

# == connect to resetpassword page ====================================================
@app.get("/resetpassword", response_class=HTMLResponse)
async def resetpassword(request: Request):
    return templates.TemplateResponse("resetpassword.html", {"request": request})

# == CLEAR DB ====================================================
@app.delete("/clear_user_db")
async def clear_user_db():
    root.instructor = BTrees.OOBTree.BTree()
    root.student = BTrees.OOBTree.BTree()
    root.otherUser = BTrees.OOBTree.BTree()
    
# == VIDEO PLAYER =====================================================================
videos_directory = Path("db/course_videos")

@app.get("/video/{course_id}/{filename}")
async def get_video(course_id: int, filename: str):
    video_path = videos_directory / str(course_id) / filename
    try:
        if not course_id in root.course.keys():
            raise HTTPException(404, detail="db_error: Course not found")

        if not root.course[course_id].isIn(Video(filename)):
            raise HTTPException(404, detail="db_error: Video not found")

        if not video_path.is_file():
            raise HTTPException(404, detail="fs_error: Video not found")

        return FileResponse(video_path, headers={"Accept-Ranges": "bytes"})
    except Exception as e:
        raise e

@app.post("/video/upload/{course_id}/{instructor_id}")
async def upload_file(course_id: int, instructor_id: int, file: UploadFile):
    course_directory = videos_directory / str(course_id)
    try:
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
    except Exception as e:
        raise e

# == USER HANDLER=======================================================================
@app.post("/user/signIn/")
async def signIn(response: Response, request: Request, id: str = Form(...), password: str = Form(...), role: str = Form(...)):
    try:
        root_db = None
        match role:
            case "student":
                root_db = root.student
                id = int(id)
            case "lecturer":
                root_db = root.instructor
                id = int(id)
            case "others":
                root_db = root.otherUser
            case _:
                raise HTTPException(404, detail="value_error: Invalid role")

        if check_user(root_db, id, password):
            access_token = signJWT(id, role)
            response.set_cookie(key="access_token", value=access_token)
            
            return RedirectResponse(url="/", status_code=302, headers={"Set-Cookie": f"access_token={access_token}; Path=/"})
        
        raise Exception 
    except Exception:
        return templates.TemplateResponse("login.html", {"request": request, "invalid": True})
  
@app.post("/user/signUp/")
async def signUp(response: Response, request: Request, id: str = Form(...), first_name: str = Form(...), last_name: str = Form(...), password: str = Form(...), role: str = Form(...)):
    try:
        if ((int(id) in root.student.keys()) or (int(id) in root.instructor.keys()) or (id in root.otherUser.keys())):
            raise HTTPException(404, detail="db_error: User already exists")
        
        match role:
            case "student":
                root_db = root.student
                id = int(id)
                root_db[id] = Student(id, first_name, last_name, password)
            case "lecturer":
                root_db = root.instructor
                id = int(id)
                root_db[id] = Instructor(id, first_name, last_name, password)
            case "others":
                root_db = root.otherUser
                root_db[id] = OtherUser(id, first_name, last_name, password)
            case _:
                raise HTTPException(404, detail="value_error: Invalid role")
            
        transaction.commit()
        
        access_token = signJWT(id, role)
        response.status_code = 200
        response.set_cookie(key="access_token", value=access_token)
        
        return RedirectResponse(url="/", status_code=302, headers={"Set-Cookie": f"access_token={access_token}; Path=/"})
    except Exception as e:
        db_error = "db_error" in str(e.detail)
        response.status_code = e.status_code
        response.set_cookie(key="access_token", value="")
        return templates.TemplateResponse("signup.html", {"request": request, "db_error": db_error})

# == USER STUDENT =======================================================================
@app.get("/user/student/{id}")
async def get_student(id: str):
    if id == "all":
        return root.student
    else:
        id = int(id)
        return root.student[id] if id in root.student.keys() else {"error": "Student not found"}

# == USER INSTRUCTOR =====================================================================
@app.get("/user/instructor/{id}")
async def get_instructor(id: str):
    if id == "all":
        return root.instructor
    else:
        id = int(id)
        return root.instructor[id] if id in root.instructor.keys() else {"error": "Instructor not found"}

# == USER OTHERS ===========================================================================
@app.get("/user/other/{username}")
async def get_other(username: str):
    if username == "all":
        return root.otherUser
    else:
        return root.otherUser[username] if username in root.otherUser.keys() else {"error": "OtherUser not found"}

# == COURSE ===========================================================================
@app.get("/course/{course_id}")
async def get_course(course_id: str):
    if course_id == "all":
        return root.course
    else:
        return root.course[int(course_id)] if int(course_id) in root.course.keys() else {"error": "Course not found"}

@app.post("/course/new/{course_id}/{name}/{instructor_id}/{public}", dependencies=[Depends(JWTBearer())])
async def post_course(course_id: str, name: str, instructor_id: str, public: bool):
    try:
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
    except Exception as e:
        raise e
    
# == CHECK TOKEN =========================================================================
@app.get("/is_token_valid")
async def is_token_valid(request: Request):
    try:
        access_token = request.cookies.get("access_token")
        if decodeJWT(access_token) != None:
            return token_response(access_token)
        raise HTTPException(status_code=401, detail="Token is invalid or expired")
    except KeyError:
        raise HTTPException(status_code=401, detail="Token not found in cookies")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")
    