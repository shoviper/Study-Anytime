from fastapi import FastAPI
from fastapi.responses import FileResponse
from pathlib import Path

app = FastAPI()

# Define the directory where your video files are stored
video_directory = Path("video_files")

@app.get("/videos/{video_filename}")
async def get_video(video_filename: str):
    # Verify that the requested video exists in the directory
    video_path = video_directory / video_filename

    if not video_path.is_file():
        return {"error": "Video not found"}

    # Serve the video file as a response
    return FileResponse(video_path)
