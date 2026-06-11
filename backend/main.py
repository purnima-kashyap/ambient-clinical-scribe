from fastapi import FastAPI
from backend.diarization.speaker_diarizer import diarize_audio

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Healthcare AI Scribe Running"}

@app.get("/diarize")
def diarize():
    return diarize_audio()