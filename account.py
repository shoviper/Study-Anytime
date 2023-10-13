import persistent

class User(persistent.Persistent):
    def __init__(self, id, first_name, second_name, password) -> None:
        self.id = id
        self.first_name = first_name
        self.second_name = second_name
        self.password = password
        self.auth = False
        
class Student(User):
    def __init__(self, id, first_name, second_name, password) -> None:
        super().__init__(id, first_name, second_name, password)
        
class Teacher(User):
    def __init__(self, id, first_name, second_name, password) -> None:
        super().__init__(id, first_name, second_name, password)
        
class Others(User):
    def __init__(self, id, first_name, second_name, password) -> None:
        super().__init__(id, first_name, second_name, password)
        
        