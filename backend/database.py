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

# == CHECK USER ========================================================================
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
