import persistent

class Video(persistent.Persistent):
    def __init__(self, title) -> None:
        self.title = title
        
    def __str__(self):
        return f"Video Title: {self.title}"

class Course(persistent.Persistent):
    def __init__(self, id, name, instructor, public) -> None:
        self.id = id
        self.name = name
        self.instructor = instructor
        self.public = public
        self.videos = []

    def __str__(self):
        return f"Course ID: {self.id}, Course Name: {self.name}, Instructor: {self.instructor}, Is Public: {self.public}, Number of Videos: {len(self.videos)}"

    def isIn(self, video):
        if any(video.title == v.title for v in self.videos):
            return True
        return False

    def addVideo(self, video):
        self.videos.append(Video(video))
