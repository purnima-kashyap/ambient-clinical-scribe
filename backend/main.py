from fastapi import FastAPI, UploadFile, File, HTTPException
from backend.diarization.speaker_diarizer import diarize_audio
from backend.asr.asr_service import transcribe_audio_with_timestamps 
import shutil
import os

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Healthcare AI Scribe Running"}

@app.get("/diarize")
def diarize():
    return diarize_audio()

@app.post("/transcribe")
async def handle_transcription(file: UploadFile = File(...)):
    temp_file_path = f"temp_{file.filename}"
    try:
        # Save uploaded file temporarily
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Pass to your ASR service
        asr_result = await transcribe_audio_with_timestamps(temp_file_path)
        return asr_result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
    finally:
        # Clean up the temp file
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)