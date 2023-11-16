import persistent

class Forum(persistent.Persistent):
    def __init__(self, user, content) -> None:
        self.user = user
        self.content = content

class Heading(Forum):
    def __init__(self, user, content) -> None:
        super().__init__(user, content)
        self.reply = []

class Video(persistent.Persistent):
    def __init__(self, title) -> None:
        self.title = title
        self.heading = []
    
    def addForum(self, forum):
        self.heading.append(forum)
    
    def __str__(self):
        return self.title

class Course(persistent.Persistent):
    def __init__(self, id, name, instructor, public) -> None:
        self.id = id
        self.name = name
        self.instructor = instructor
        self.public = public
        self.videos = []
        self.student_list = []

    def __str__(self):
        return f"Course ID: {self.id}, Course Name: {self.name}, Instructor: {self.instructor}, Is Public: {self.public}, Number of Videos: {len(self.videos)}"

    def isIn(self, video):
        if any(video.title == v.title for v in self.videos):
            return True
        return False

    def addVideo(self, video):
        self.videos.append(video)
        
    def enrollStudent(self, student_id):
        self.student_list.append(student_id)
