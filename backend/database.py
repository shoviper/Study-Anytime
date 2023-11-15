import ZODB, ZODB.FileStorage
import BTrees.OOBTree

from course import *
from user import *

storage = ZODB.FileStorage.FileStorage("db/data.fs")
db = ZODB.DB(storage)
connection = db.open()
root = connection.root

if not hasattr(root, "course"):
    root.course = BTrees.OOBTree.BTree()
if not hasattr(root, "instructor"):
    root.instructor = BTrees.OOBTree.BTree()
if not hasattr(root, "student"):
    root.student = BTrees.OOBTree.BTree()
if not hasattr(root, "otherUser"):
    root.otherUser = BTrees.OOBTree.BTree()

# == USER ========================================================================
def check_user(root_class, id, pwd):
    if root_class[id].password == pwd:
        return True
    return False

def get_user(id):
    if id in root.student.keys():
        return root.student[id]
    elif id in root.instructor.keys():
        return root.instructor[id]
    elif id in root.otherUser.keys():
        return root.otherUser[id]
    
    return Exception


# == COURSE ========================================================================
def get_all_courses(user_id, rootdb):
    return [course for course in rootdb[user_id].courses]

def get_course(id):
    if id in root.course.keys():
        return root.course[id]
    
    return Exception("Course Does not Exist")

def get_video_names(course):
    names = []
    for video in course.videos:
        names.append(str(video.title))
        
    return names

def get_video(course_id, video_name):
    for video in root.course[course_id].videos:
        print(video.__dict__)
        if video_name == video.title:
            return video
    return []

def isCourseValid(user_id, course_id):
    if root.course[course_id].public:
        return True
    
    return True if course_id in get_user(user_id).courses else False