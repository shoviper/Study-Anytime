import os
import shutil
from typing import Optional
from fastapi import FastAPI, Request, Response, UploadFile, HTTPException, Cookie, Query, Form
from fastapi.responses import HTMLResponse, RedirectResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from database import *
from auth.auth_handler import *

import transaction
import logging

app = FastAPI()
templates = Jinja2Templates(directory="templates")
logging.basicConfig(level=logging.DEBUG)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)

app.mount("/static", StaticFiles(directory="static"), name="static")


# == connect to main(default) page ============================================================
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request, access_token: str = Cookie(None)):
    try:
        token = decodeJWT(access_token)
        id = token["id"]
        role = token["role"]
        username = f"{get_user(id).first_name} {get_user(id).last_name}"
        return templates.TemplateResponse("index.html", {"request": request, "alreadylogin": True, "username": username, "role": role})
    except:
        return templates.TemplateResponse("index.html", {"request": request, "alreadylogin": False})
    
@app.on_event("shutdown")
async def shutdown():
    transaction.commit()
    db.close()

# == connect to login page ============================================================
@app.get("/login", response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request, "invalid": False})

# == connect to sign up page ==========================================================
@app.get("/signup", response_class=HTMLResponse)
async def signup(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request, "invalid": False})

# == connect to resetpassword page ====================================================
@app.get("/resetpassword", response_class=HTMLResponse)
async def resetpassword(request: Request):
    return templates.TemplateResponse("resetpassword.html", {"request": request, "sent": False})

# == connect to logout page ============================================================
@app.get("/logout", response_class=HTMLResponse)
async def logout(response: Response, request: Request):
    response.delete_cookie("access_token")
    return RedirectResponse(url="/", status_code=302, headers={"Set-Cookie": f"access_token={None}; Path=/"})

# == connect to about page ============================================================
@app.get("/about", response_class=HTMLResponse)
async def about(request: Request, access_token: str = Cookie(None)):
    try:
        token = decodeJWT(access_token)
        id = token["id"]
        role = token["role"]
        username = f"{get_user(id).first_name} {get_user(id).last_name}"
        return templates.TemplateResponse("about.html", {"request": request, "alreadylogin": True, "username": username, "role": role})
    except:
        return templates.TemplateResponse("about.html", {"request": request, "alreadylogin": False})

# == connect to admission page ============================================================
@app.get("/admission", response_class=HTMLResponse)
async def admission(request: Request, access_token: str = Cookie(None)):
    try:
        token = decodeJWT(access_token)
        id = token["id"]
        role = token["role"]
        username = f"{get_user(id).first_name} {get_user(id).last_name}"
        return templates.TemplateResponse("admission.html", {"request": request, "alreadylogin": True, "username": username, "role": role})
    except:
        return templates.TemplateResponse("admission.html", {"request": request, "alreadylogin": False})

# == connect to news page ============================================================
@app.get("/news", response_class=HTMLResponse)
async def news(request: Request, access_token: str = Cookie(None)):
    try:
        token = decodeJWT(access_token)
        id = token["id"]
        role = token["role"]
        username = f"{get_user(id).first_name} {get_user(id).last_name}"
        return templates.TemplateResponse("news.html", {"request": request, "alreadylogin": True, "username": username, "role": role})
    except:
        return templates.TemplateResponse("news.html", {"request": request, "alreadylogin": False})

@app.get("/news1", response_class=HTMLResponse)
async def news(request: Request, access_token: str = Cookie(None)):
    try:
        token = decodeJWT(access_token)
        id = token["id"]
        role = token["role"]
        username = f"{get_user(id).first_name} {get_user(id).last_name}"
        return templates.TemplateResponse("news1.html", {"request": request, "alreadylogin": True, "username": username, "role": role})
    except:
        return templates.TemplateResponse("news1.html", {"request": request, "alreadylogin": False})

@app.get("/news2", response_class=HTMLResponse)
async def news(request: Request, access_token: str = Cookie(None)):
    try:
        token = decodeJWT(access_token)
        id = token["id"]
        role = token["role"]
        username = f"{get_user(id).first_name} {get_user(id).last_name}"
        return templates.TemplateResponse("news2.html", {"request": request, "alreadylogin": True, "username": username, "role": role})
    except:
        return templates.TemplateResponse("news2.html", {"request": request, "alreadylogin": False})

@app.get("/news3", response_class=HTMLResponse)
async def news(request: Request, access_token: str = Cookie(None)):
    try:
        token = decodeJWT(access_token)
        id = token["id"]
        role = token["role"]
        username = f"{get_user(id).first_name} {get_user(id).last_name}"
        return templates.TemplateResponse("news3.html", {"request": request, "alreadylogin": True, "username": username, "role": role})
    except:
        return templates.TemplateResponse("news3.html", {"request": request, "alreadylogin": False})

@app.get("/news4", response_class=HTMLResponse)
async def news(request: Request, access_token: str = Cookie(None)):
    try:
        token = decodeJWT(access_token)
        id = token["id"]
        role = token["role"]
        username = f"{get_user(id).first_name} {get_user(id).last_name}"
        return templates.TemplateResponse("news4.html", {"request": request, "alreadylogin": True, "username": username, "role": role})
    except:
        return templates.TemplateResponse("news4.html", {"request": request, "alreadylogin": False})

# == connect to program page ============================================================
@app.get("/se2022", response_class=HTMLResponse)
async def se2022(request: Request, access_token: str = Cookie(None)):
    try:
        token = decodeJWT(access_token)
        id = token["id"]
        role = token["role"]
        username = f"{get_user(id).first_name} {get_user(id).last_name}"
        return templates.TemplateResponse("se2022.html", {"request": request, "alreadylogin": True, "username": username, "role": role})
    except:
        return templates.TemplateResponse("se2022.html", {"request": request, "alreadylogin": False})

@app.get("/se2024", response_class=HTMLResponse)
async def se2024(request: Request, access_token: str = Cookie(None)):
    try:
        token = decodeJWT(access_token)
        id = token["id"]
        role = token["role"]
        username = f"{get_user(id).first_name} {get_user(id).last_name}"
        return templates.TemplateResponse("se2024.html", {"request": request, "alreadylogin": True, "username": username, "role": role})
    except:
        return templates.TemplateResponse("se2024.html", {"request": request, "alreadylogin": False})

@app.get("/glasgow", response_class=HTMLResponse)
async def glasgow(request: Request, access_token: str = Cookie(None)):
    try:
        token = decodeJWT(access_token)
        id = token["id"]
        role = token["role"]
        username = f"{get_user(id).first_name} {get_user(id).last_name}"
        return templates.TemplateResponse("glasgow.html", {"request": request, "alreadylogin": True, "username": username, "role": role})
    except:
        return templates.TemplateResponse("glasgow.html", {"request": request, "alreadylogin": False})
    
@app.get("/queensland", response_class=HTMLResponse)
async def queensland(request: Request, access_token: str = Cookie(None)):
    try:
        token = decodeJWT(access_token)
        id = token["id"]
        role = token["role"]
        username = f"{get_user(id).first_name} {get_user(id).last_name}"
        return templates.TemplateResponse("queensland.html", {"request": request, "alreadylogin": True, "username": username, "role": role})
    except:
        return templates.TemplateResponse("queensland.html", {"request": request, "alreadylogin": False})



# == connect to studyanytime page ============================================================
@app.get("/studyanytime", response_class=HTMLResponse)
async def studyanytime(request: Request, access_token: str = Cookie(None)):
    try:
        token = decodeJWT(access_token)
        id = token["id"]
        role = token["role"]
        user = get_user(id)
        username = f"{user.first_name} {user.last_name}"
        
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
        
        enrolled_courses = [root.course[c] for c in get_all_courses(id, root_db)]
        enrolled = [enroll for enroll in enrolled_courses if enroll.id in user.courses]
        other_courses = [root.course[c] for c in root.course]
        other = [o for o in other_courses if o.id not in user.courses]
        instructor_db = root.instructor
        
        return templates.TemplateResponse("studyanytime.html", {"request": request, "alreadylogin": True, "username": username, "role": role, "enrolled" : enrolled, "other": other, "instructor_db": instructor_db})
    except Exception as e:
        print(e)
        return templates.TemplateResponse("studyanytime.html", {"request": request, "alreadylogin": False})

@app.get("/studyanytime/course/{course_id}", response_class=HTMLResponse)
async def studyanytime(request: Request, course_id : str, access_token : str = Cookie(None)):
    try:
        token = decodeJWT(access_token)
        id = token["id"]
        role = token["role"]
        username = f"{get_user(id).first_name} {get_user(id).last_name}"
        course = await get_course(int(course_id))
        videos = get_video_names(course)
        isInstructor = True if course.instructor == id else False
        isPublic = course.public
        enrolled = True if id in course.student_list or course.public else False
        student_list = [get_user(name) for name in course.student_list]
        
        return templates.TemplateResponse("course.html", {"request": request, "alreadylogin": True, "username": username, "role": role, "course_id": course_id, "isInstructor": isInstructor, "isPublic": isPublic, "enrolled": enrolled, "videos": videos, "student_list": student_list})
    except Exception as e:
        print(e)
        return templates.TemplateResponse("course.html", {"request": request, "alreadylogin": False})

@app.get("/studyanytime/course/video/{course_id}/{video_name}", response_class=HTMLResponse)
async def studyanytime(request: Request, course_id : int, video_name : str, access_token : str = Cookie(None)):
    try:
        token = decodeJWT(access_token)
        id = token["id"]
        role = token["role"]
        username = f"{get_user(id).first_name} {get_user(id).last_name}"
        
        course = await get_course(course_id)
        forum = []
        
        for video in course.videos:
            if video_name == video.title:
                forum = video.heading
                break
        
        return templates.TemplateResponse("videoplayer.html", {"request": request, "alreadylogin": True, "username": username, "role": role, "course": course, "video_name": video_name, "forum" : forum})
    except Exception as e:
        print(e)
        return templates.TemplateResponse("videoplayer.html", {"request": request, "alreadylogin": False})
    

# == CLEAR DB ====================================================
@app.delete("/clear_user_db")
async def clear_user_db():
    root.instructor = BTrees.OOBTree.BTree()
    root.student = BTrees.OOBTree.BTree()
    root.otherUser = BTrees.OOBTree.BTree()
    
@app.delete("/clear_course_db")
async def clear_course_db():
    root.course = BTrees.OOBTree.BTree()
    
    shutil.rmtree(VIDEO_DIR, ignore_errors=True)
    os.makedirs(VIDEO_DIR, exist_ok=True)

# == VERIFY JWT ====================================================
@app.get("/verify_token")
async def verify_token(request: Request, access_token: str = Cookie(None)):
    if decodeJWT(access_token) == None:
        return False
    else:
        return True

# == VIDEO PLAYER =====================================================================
VIDEO_DIR = Path("db/course_videos")

@app.get("/video/{course_id}/{video_name}")
async def get_video(course_id: int, video_name: str):
    video_path = VIDEO_DIR / str(course_id) / video_name
    try:
        if not course_id in root.course.keys():
            raise HTTPException(404, detail="db_error: Course not found")

        if not root.course[course_id].isIn(Video(video_name)):
            raise HTTPException(404, detail="db_error: Video not found")

        if not video_path.is_file():
            raise HTTPException(404, detail="fs_error: Video not found")

        video_size = video_path.stat().st_size

        def iter_file():
            with open(video_path, "rb") as video_file:
                while chunk := video_file.read(65536):  # Adjust the chunk size as needed
                    yield chunk

        return StreamingResponse(iter_file(), media_type="video/mp4", headers={"Accept-Ranges": "bytes", "Content-Length": str(video_size)})

    except Exception as e:
        print(e)
        raise e

@app.post("/video/upload/{course_id}")
async def delete_file(request: Request, course_id: int, file: UploadFile, access_token : str = Cookie(None)):
    COURSE_DIR = VIDEO_DIR / str(course_id)
    try:
        token = decodeJWT(access_token)
        id = token["id"]
        role = token["role"]
        username = f"{get_user(id).first_name} {get_user(id).last_name}"
        course = await get_course(int(course_id))
        videos = get_video_names(course)
        isInstructor = True if course.instructor == id else False
        isPublic = course.public
        enrolled = True if id in course.student_list or course.public else False
        student_list = [get_user(name) for name in course.student_list]
        
        if not id in root.instructor.keys():
            raise HTTPException(404, detail="db_error: Instructor not found")

        file_path = COURSE_DIR / file.filename

        if root.course[course_id].isIn(Video(file.filename)):
            raise HTTPException(404, detail="db_error: Video with the same filename already exists")

        if file_path.is_file():
            raise HTTPException(404, detail="fs_error: Video with the same filename already exists")

        with open(file_path, "wb") as f:
            f.write(file.file.read())

        temp_course = Course(root.course[course_id].id, root.course[course_id].name, root.course[course_id].instructor, root.course[course_id].public)    
        for c in root.course[course_id].videos:
            temp_course.addVideo(c)
        temp_course.addVideo(Video(file.filename))
        
        for c in root.course[course_id].student_list:
            temp_course.enrollStudent(c)
        root.course[course_id] = temp_course
        
        transaction.commit()
        return RedirectResponse(url=f"/studyanytime/course/{course_id}", status_code=302, headers={"Set-Cookie": f"access_token={access_token}; Path=/"})
    except Exception as e:
        print(e)
        return templates.TemplateResponse("course.html", {"request": request, "alreadylogin": True, "username": username, "role": role, "course_id": course_id, "isInstructor": isInstructor, "isPublic": isPublic, "enrolled": enrolled, "videos": videos, "student_list": student_list})
    
@app.post("/video/delete/{course_id}/{video_name}")
async def delete_file(request: Request, course_id: int, video_name: str, access_token : str = Cookie(None)):
    COURSE_DIR = VIDEO_DIR / str(course_id)
    try:
        token = decodeJWT(access_token)
        instructor_id = token["id"]
        course = await get_course(int(course_id))
        
        if instructor_id != course.instructor:
            raise HTTPException(404, detail="permission_error: Invalid access")

        file_path = COURSE_DIR / video_name

        if not (root.course[course_id].isIn(Video(video_name))):
            raise HTTPException(404, detail="db_error: Video does not exist")

        if not file_path.is_file():
            raise HTTPException(404, detail="fs_error: Video does not exist")

        os.remove(file_path)

        temp_course = Course(root.course[course_id].id, root.course[course_id].name, root.course[course_id].instructor, root.course[course_id].public)    
        for c in root.course[course_id].videos:
            if c.title != video_name:
                temp_course.addVideo(c)
        
        for c in root.course[course_id].student_list:
            temp_course.enrollStudent(c)
        root.course[course_id] = temp_course
        
        transaction.commit()
        return RedirectResponse(url=f"/studyanytime/course/{course_id}", status_code=302, headers={"Set-Cookie": f"access_token={access_token}; Path=/"})
    except Exception as e:
        print(e)
        raise e
    
@app.post("/video/{course_id}/{video_name}", response_class=HTMLResponse)
async def add_comment(request: Request, course_id: int, video_name: str, post_content: str = Form(...), access_token: str = Cookie(None)):
    token = decodeJWT(access_token)
    id = token["id"]
    role = token["role"]
    username = f"{get_user(id).first_name} {get_user(id).last_name}"
    
    temp_course = Course(root.course[course_id].id, root.course[course_id].name, root.course[course_id].instructor, root.course[course_id].public)
    for video in root.course[course_id].videos:
        temp_video = Video(video.title)
        for h in video.heading:
            temp_heading = Heading(h.user, h.content)
            for f in h.reply:
                temp_heading.reply.append(f)
            temp_video.addForum(temp_heading)
            
        if video_name == video.title:
            temp_video.addForum(Heading(id, post_content))
            forum = temp_video.heading
            
        temp_course.addVideo(temp_video)
    
    for c in root.course[course_id].student_list:
        temp_course.enrollStudent(c)
        
    root.course[course_id] = temp_course
    course = await get_course(course_id)
    transaction.commit()
    
    return templates.TemplateResponse("videoplayer.html", {"request": request, "alreadylogin": True, "username": username, "role": role, "course": course, "video_name": video_name, "forum" : forum})

@app.post("/video/{course_id}/{video_name}/{heading_no}", response_class=HTMLResponse)
async def add_reply(request: Request, course_id: int, video_name: str, heading_no: int, post_content: str = Form(...), access_token: str = Cookie(None)):
    token = decodeJWT(access_token)
    id = token["id"]
    role = token["role"]
    username = f"{get_user(id).first_name} {get_user(id).last_name}"
    
    temp_course = Course(root.course[course_id].id, root.course[course_id].name, root.course[course_id].instructor, root.course[course_id].public)
    for video in root.course[course_id].videos:
        count = 0
        temp_video = Video(video.title)
        for h in video.heading:
            temp_heading = Heading(h.user, h.content)
            for f in h.reply:
                temp_heading.reply.append(f)
            
            if video_name == video.title and count == heading_no:
                temp_heading.reply.append(Forum(id, post_content))
                
            temp_video.addForum(temp_heading)
                
            count += 1
            
        temp_course.addVideo(temp_video)
    
    for c in root.course[course_id].student_list:
        temp_course.enrollStudent(c)
    root.course[course_id] = temp_course
    
    transaction.commit()
    
    return RedirectResponse(url=f"/studyanytime/course/video/{course_id}/{video_name}", status_code=302, headers={"Set-Cookie": f"access_token={access_token}; Path=/"})

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
async def signUp(response: Response, request: Request, id: str = Form(...), first_name: str = Form(...), last_name: str = Form(...), email: str = Form(...), password: str = Form(...), role: str = Form(...)):
    try:
        if id.isnumeric():
            if (int(id) in root.student.keys()) or (int(id) in root.instructor.keys()):
                raise HTTPException(404, detail="db_error: User already exists")
        else:
            if id in root.otherUser.keys():
                raise HTTPException(404, detail="db_error: User already exists")
            
        match role:
            case "student":
                root_db = root.student
                id = int(id)
                root_db[id] = Student(id, first_name, last_name, email, password)
            case "lecturer":
                root_db = root.instructor
                id = int(id)
                root_db[id] = Instructor(id, first_name, last_name, email, password)
            case "others":
                root_db = root.otherUser
                root_db[id] = OtherUser(id, first_name, last_name, email, password)
            case _:
                raise HTTPException(404, detail="value_error: Invalid role")
        
        transaction.commit()
        
        access_token = signJWT(id, role)
        response.status_code = 200
        response.set_cookie(key="access_token", value=access_token)
        
        return RedirectResponse(url="/", status_code=302, headers={"Set-Cookie": f"access_token={access_token}; Path=/"})
    except Exception as e:
        print(e)
        return templates.TemplateResponse("signup.html", {"request": request, "invalid": True})

from reset_pwd import*

@app.get("/user/resetPwd/")
async def resetPwd(request: Request, email: str = Query(...)):
    try:
        found = False
        
        for u in root.student:
            user = get_user(u)
            if email == user.email:
                found = user
                break
        
        if not found:
            for u in root.instructor:
                user = get_user(u)
                if email == user.email:
                    found = user
                    break
        
        if not found:
            for u in root.otherUser:
                user = get_user(u)
                if email == user.email:
                    found = user
                    break
        
        if not found:
            raise Exception("User not found") 
        
        payload = {
            "id" : user.id,
            "exp" : time.time() + 600
        }
        token = jwt.encode(payload, SECRET_KEY, ALGORITHM)
        
        reciever_email = email
        body = f"click this link to reset your password: \nhttp://127.0.0.1:8000/user/resetPwd/{token}\n\nThis link will be valid only for 10 mins."
        email_body = MIMEText(body, "plain")
        
        message = MIMEMultipart()
        message["From"] = SENDER_EMAIL
        message["To"] = reciever_email
        message["Subject"] = SUBJECT
        message.attach(email_body)

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.sendmail(SENDER_EMAIL, reciever_email, message.as_string())

        print("Email sent successfully!")
        
        print(found)
        return templates.TemplateResponse("resetpassword.html", {"request": request, "sent": True})
    except Exception as e:
        print(e)
        return templates.TemplateResponse("resetpassword.html", {"request": request, "sent": True})

@app.get("/user/resetPwd/{token}")
async def redirectToResetPwd(request: Request, token: str):
    return templates.TemplateResponse("newpass.html", {"request": request, "token": token})
         
@app.post("/user/resetPwd/{token}")
async def resetPwd(request: Request, token: str, new_password: str = Form(...)):
    try:
        id = decodeJWT(token)["id"]
        user = get_user(id)
        
        user.password = new_password
        
        transaction.commit()
        return RedirectResponse(url="/login", status_code=302)
    except Exception as e:
        print(e)
        return RedirectResponse(url="/", status_code=302)

@app.post("/enroll/{course_id}")
async def enroll(course_id: int, student_id: str = Form(...), access_token : str = Cookie(None)):
    try:
        user = get_user(int(student_id))
        if course_id in user.courses:
            raise HTTPException(404, detail="Already Enrolled")
        
        course = await get_course(course_id)

        student_id = int(student_id)
        temp_user = Student(root.student[student_id].id, root.student[student_id].first_name, root.student[student_id].last_name, root.student[student_id].email, root.student[student_id].password)
        for c in root.student[student_id].courses:
            temp_user.enrollCourse(c)
        temp_user.enrollCourse(course.id)
        root.student[student_id] = temp_user
            
        temp_course = Course(root.course[course_id].id, root.course[course_id].name, root.course[course_id].instructor, root.course[course_id].public)
        for c in root.course[course_id].student_list:
            temp_course.enrollStudent(c)
        temp_course.enrollStudent(student_id)
        
        for c in root.course[course_id].videos:
            temp_course.addVideo(c)
        root.course[course_id] = temp_course
        
        transaction.commit()
        return RedirectResponse(url=f"/studyanytime/course/{course_id}", status_code=302, headers={"Set-Cookie": f"access_token={access_token}; Path=/"})
    except Exception as e:
        print(e)
        return RedirectResponse(url=f"/studyanytime/course/{course_id}", status_code=302, headers={"Set-Cookie": f"access_token={access_token}; Path=/"})

@app.post("/withdraw/{course_id}/{student_id}")
async def withdraw(course_id: int, student_id: int, access_token : str = Cookie(None)):
    try:
        user = get_user(student_id)
        temp_user = Student(user.id, user.first_name, user.last_name, user.email, user.password)
        for c in user.courses:
            temp_user.enrollCourse(c)
        temp_user.courses.remove(course_id)
        root.student[student_id] = temp_user
        print(temp_user.__dict__)
        
        course = await get_course(course_id)
        temp_course = Course(course.id, course.name, course.instructor, course.public)
        for c in root.course[course_id].student_list:
            temp_course.enrollStudent(c)
        temp_course.student_list.remove(student_id)
        root.course[course_id] = temp_course
        print(temp_course.__dict__)
        
        transaction.commit()
        return RedirectResponse(url=f"/studyanytime/course/{course_id}", status_code=302, headers={"Set-Cookie": f"access_token={access_token}; Path=/"})
    except Exception as e:
        print(e)
        return RedirectResponse(url=f"/studyanytime/course/{course_id}", status_code=302, headers={"Set-Cookie": f"access_token={access_token}; Path=/"})
     

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

@app.post("/course/new/", response_class=HTMLResponse)
async def post_course(request: Request, course_id: str = Form(...), course_name: str = Form(...), course_public: Optional[str] = Form(default="off"), access_token: str = Cookie(None)):
    try:
        token = decodeJWT(access_token)
        instructor_id = token["id"]
        is_public = course_public.lower() == "on"
        if int(course_id) in root.course.keys():
            raise HTTPException(404, detail="db_error: Course already exists")

        if not int(instructor_id) in root.instructor.keys():
            raise HTTPException(404, detail="db_error: Instructor not found")
        
        course_directory = VIDEO_DIR / course_id
        course_directory.mkdir(parents=True)
        
        root.course[int(course_id)] = Course(int(course_id), course_name, instructor_id, is_public)
        
        temp_instructor = Instructor(int(instructor_id), root.instructor[int(instructor_id)].first_name, root.instructor[int(instructor_id)].last_name, root.instructor[int(instructor_id)].email, root.instructor[int(instructor_id)].password)
        for c in root.instructor[int(instructor_id)].courses:
            temp_instructor.enrollCourse(c)
        temp_instructor.enrollCourse(int(course_id))
        root.instructor[int(instructor_id)] = temp_instructor
        
        transaction.commit()

        return RedirectResponse(url="/studyanytime", status_code=302, headers={"Set-Cookie": f"access_token={access_token}; Path=/"})
    except Exception as e:
        print(e)
        return RedirectResponse(url="/studyanytime", status_code=302, headers={"Set-Cookie": f"access_token={access_token}; Path=/"})
    
@app.post("/course/remove/{course_id}", response_class=HTMLResponse)
async def remove_course(request: Request, course_id: int, access_token: str = Cookie(None)):
    COURSE_DIR = VIDEO_DIR / str(course_id)
    try:
        token = decodeJWT(access_token)
        instructor_id = token["id"]
        course = await get_course(course_id)
        if course_id not in root.course.keys():
            raise HTTPException(404, detail="db_error: Course does not already exists")

        if instructor_id != course.instructor:
            raise HTTPException(404, detail="permission_error: Invalid access")
        
        for s in root.student:
            student = root.student[s]
            temp_user = Student(student.id, student.first_name, student.last_name, student.email, student.password)
            for c in student.courses:
                temp_user.enrollCourse(c)
                
            if course_id in temp_user.courses: 
                temp_user.courses.remove(course_id)
                
            root.student[s] = temp_user
                
        for i in root.instructor:
            instructor = root.instructor[i]
            temp_user = Instructor(instructor.id, instructor.first_name, instructor.last_name, instructor.email, instructor.password)
            for c in instructor.courses:
                temp_user.enrollCourse(c)
            
            if course_id in temp_user.courses:
                temp_user.courses.remove(course_id)
                
            root.instructor[i] = temp_user
        
        root.course.pop(course_id)
        shutil.rmtree(COURSE_DIR, ignore_errors=True)
        
        transaction.commit()

        return RedirectResponse(url="/studyanytime", status_code=302, headers={"Set-Cookie": f"access_token={access_token}; Path=/"})
    except Exception as e:
        print(e)
        return RedirectResponse(url="/studyanytime", status_code=302, headers={"Set-Cookie": f"access_token={access_token}; Path=/"})
    
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
