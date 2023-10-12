from fastapi import FastAPI, UploadFile
from fastapi.responses import FileResponse
from pathlib import Path

app = FastAPI()

directory = Path("video_files")

@app.get("/videos/{video_filename}")
async def get_video(video_filename: str):
    video_path = directory / video_filename

    if not video_path.is_file():
        return {"error": "Video not found"}

    return FileResponse(video_path, headers={"Accept-Ranges": "bytes"})

@app.post("/upload/")
async def upload_file(file: UploadFile):
    
    with open(f"{directory}/{file.filename}", "wb") as f:
        f.write(file.file.read())