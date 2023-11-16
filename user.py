import persistent

class User(persistent.Persistent):
    def __init__(self, first_name, last_name, email, password) -> None:
        self.first_name = first_name
        self.last_name = last_name
        self.password = password
        self.email = email
        self.courses = []
        
    def enrollCourse(self, course):
        self.courses.append(course)

class Instructor(User):
    def __init__(self, id, first_name, last_name, email, password) -> None:
        super().__init__(first_name, last_name, email, password)
        self.id = id
        
    def __str__(self):
        return f" ID: {self.id}, {self.first_name} {self.last_name}, Number of courses: {len(self.courses)}"

class Student(User):
    def __init__(self, id, first_name, last_name, email, password) -> None:
        super().__init__(first_name, last_name, email, password)
        self.id = id
        
    def __str__(self):
        return f"ID: {self.id}, {self.first_name} {self.last_name}, Number of enrolls: {len(self.courses)}"

class OtherUser(User):
    def __init__(self, username, first_name, last_name, email, password) -> None:
        super().__init__(first_name, last_name, email, password)
        self.username = username
        
    def __str__(self):
        return f"Username: {self.username}, {self.first_name} {self.last_name}, Number of enrolls: {len(self.enrolls)}"
