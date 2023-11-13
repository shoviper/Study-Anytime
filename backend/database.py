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

def get_course(id):
    if id in root.course.keys():
        return root.course[id]
    
    return Exception

# == COURSE ========================================================================
def get_course_names(user_id, rootdb):
    course_list = []
    for course in rootdb[user_id].courses:
        course_list[course.id] = course.name
    
    return course_list

def get_video_names(course):
    names = []
    for video in course.videos:
        names.append(video.title)
        
    return names

def isCourseValid(user_id, course_id):
    if root.course[course_id].public:
        return True
    
    return True if course_id in get_user(user_id).courses else False