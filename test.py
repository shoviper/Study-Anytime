from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
from pathlib import Path

app = FastAPI()
video_directory = Path("video_files")

@app.get("/videos/{video_filename}")
async def get_video(video_filename: str, range: str = None):
    video_path = video_directory / video_filename

    if not video_path.is_file():
        raise HTTPException(status_code=404, detail="Video not found")

    start, end = 0, video_path.stat().st_size
    if range:
        try:
            start, end = map(int, range.strip("bytes=").split("-"))
        except ValueError:
            pass

    content_length = end - start + 1

    with open(video_path, "rb") as video_file:
        video_file.seek(start)
        chunk_size = 65536  # Adjust chunk size as needed
        content = video_file.read(chunk_size)
        while content:
            yield content
            content = video_file.read(chunk_size)

@app.post("/upload/")
async def upload_file(file: UploadFile):
    with open(video_directory / file.filename, "wb") as f:
        f.write(file.file.read()) 