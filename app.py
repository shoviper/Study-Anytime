from fastapi import FastAPI
from fastapi.responses import FileResponse
from pathlib import Path

app = FastAPI()

video_directory = Path("video_files")

@app.get("/videos/{video_filename}")
async def get_video(video_filename: str):
    video_path = video_directory / video_filename

    if not video_path.is_file():
        return {"error": "Video not found"}

    return FileResponse(video_path, headers={"Accept-Ranges": "bytes"})
