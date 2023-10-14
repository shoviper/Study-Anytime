import persistent
from course import *

class User(persistent.Persistent):
    def __init__(self, first_name, last_name, password) -> None:
        self.first_name = first_name
        self.last_name = last_name
        self.password = password
        self.auth = False

class Instructor(User):
    def __init__(self, id, first_name, last_name, password) -> None:
        super().__init__(first_name, last_name, password)
        self.id = id
        self.courses = []

    def addCourse(self, course: Course):
        self.courses.append(course)

class Student(User):
    def __init__(self, id, first_name, last_name, password) -> None:
        super().__init__(first_name, last_name, password)
        self.id = id
        self.enrolls = []

    def enrollCourse(self, course: Course):
        self.enrolls.append(course)

class OtherUser(User):
    def __init__(self, username, first_name, last_name, password) -> None:
        super().__init__(first_name, last_name, password)
        self.username = username
        self.enrolls = []

    def enrollCourse(self, course: Course):
        if not course.public:
            return "this course is not public"

        self.enrolls.append(course)
