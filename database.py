import ZODB, ZODB.FileStorage
import BTrees.OOBTree

from course import *
from user import *

storage = ZODB.FileStorage.FileStorage("db/data.fs")
db = ZODB.DB(storage)
connection = db.open()
root = connection.root

if not hasattr(root, 'course'):
    root.course = BTrees.OOBTree.BTree()
if not hasattr(root, 'instructor'):
    root.instructor = BTrees.OOBTree.BTree()
if not hasattr(root, 'student'):
    root.student = BTrees.OOBTree.BTree()
if not hasattr(root, 'otherUser'):
    root.otherUser = BTrees.OOBTree.BTree()