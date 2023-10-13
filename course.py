import persistent
        
class Video:
    def __init__(self, title) -> None:
        self.title = title
        
class Course(persistent.Persistent):
    def __init__(self, id, name, instructor, public) -> None:
        self.id = id
        self.name = name
        self.instructor = instructor
        self.public = public
        self.videos = []
        
    def addVideo(self, video: Video):
        if any(video.title == v.title for v in self.videos):
            return print("Video already existed")
        
        self.videos.append(video)
