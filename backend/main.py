from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from backend.diarization.speaker_diarizer import diarize_audio
from backend.asr.asr_service import transcribe_audio_with_timestamps 
from backend.llm.llm_service import generate_soap_note
from backend.vector_db.search import search_icd
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
        
        # Pass to the ASR service
        asr_result = await transcribe_audio_with_timestamps(temp_file_path)
        return asr_result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
    finally:
        # Clean up the temp file
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)


class TranscriptRequest(BaseModel):
    transcript: str

class ICDRequest(BaseModel):
    query: str

@app.post("/generate-soap")
async def handle_soap_generation(request: TranscriptRequest):
    """
    Takes a raw text transcript and returns a structured JSON SOAP note.
    """
    try:
        # Pass the string straight to the new LangChain service
        soap_result = await generate_soap_note(request.transcript)
        return soap_result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/recommend-icd")
async def recommend_icd(request: ICDRequest):
    """
    Returns the most relevant ICD-10 codes.
    """

    try:

        results = search_icd(request.query)

        return {"recommendations": results}

    except Exception as e:

        raise HTTPException(status_code=500, detail=str(e))