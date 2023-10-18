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

# import os
# import ZODB.FileStorage
# import BTrees.OOBTree

# from course import *
# from user import *

# db_directory = "db"

# # Ensure that the directory exists
# if not os.path.exists(db_directory):
#     os.makedirs(db_directory)

# storage = ZODB.FileStorage.FileStorage(os.path.join(db_directory, "data.fs"))
# db = ZODB.DB(storage)
# connection = db.open()
# root = connection.root

# if not hasattr(root, "course"):
#     root.course = BTrees.OOBTree.BTree()
# if not hasattr(root, "instructor"):
#     root.instructor = BTrees.OOBTree.BTree()
# if not hasattr(root, "student"):
#     root.student = BTrees.OOBTree.BTree()
# if not hasattr(root, "otherUser"):
#     root.otherUser = BTrees.OOBTree.BTree()
