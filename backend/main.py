from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from backend.diarization.speaker_diarizer import diarize_audio
from backend.asr.asr_service import transcribe_audio_with_timestamps 
from backend.vector_db.search import search_icd
from backend.storage.cloudinary_service import upload_audio_to_cloudinary
from backend.llm.llm_service import SOAPNoteGenerator

import os
import uuid
import asyncio

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

soap_generator = SOAPNoteGenerator()

ALLOWED_EXTENSIONS = {".wav", ".mp3", ".m4a", ".webm", ".ogg"}
MAX_FILE_SIZE = 25 * 1024 * 1024  # 25 MB
TEMP_DIR = "temp_uploads"
os.makedirs(TEMP_DIR, exist_ok=True)


@app.get("/")
def home():
    return {"message": "Healthcare AI Scribe Running"}


@app.get("/diarize")
def diarize():
    return diarize_audio()


async def _save_upload(file: UploadFile, temp_file_path: str) -> int:
    """Streams the upload to disk, enforcing the size limit. Returns bytes written."""
    size = 0
    with open(temp_file_path, "wb") as buffer:
        while chunk := await file.read(1024 * 1024):
            size += len(chunk)
            if size > MAX_FILE_SIZE:
                raise HTTPException(
                    status_code=400,
                    detail=f"File exceeds max size of {MAX_FILE_SIZE // (1024*1024)}MB"
                )
            await asyncio.to_thread(buffer.write, chunk)
    return size


@app.post("/process-consultation")
async def process_consultation(file: UploadFile = File(...)):
    """
    Full pipeline for one consultation:
    1. Save uploaded audio temporarily
    2. Upload audio to Cloudinary (permanent storage, returns hosted URL)
    3. Transcribe audio locally with Whisper
    4. Generate a structured SOAP note from the transcript
    5. Delete the local temp copy (Cloudinary copy remains)
    """
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type '{ext}'. Allowed: {', '.join(sorted(ALLOWED_EXTENSIONS))}"
        )

    consultation_id = uuid.uuid4().hex
    temp_file_path = os.path.join(TEMP_DIR, f"{consultation_id}{ext}")

    try:
        # --- Step 1: Save locally (temporary) ---
        size = await _save_upload(file, temp_file_path)
        if size == 0:
            raise HTTPException(status_code=400, detail="Uploaded file is empty.")

        # --- Step 2: Upload to Cloudinary ---
        try:
            audio_data = await upload_audio_to_cloudinary(temp_file_path, public_id=consultation_id)
        except RuntimeError as e:
            raise HTTPException(status_code=502, detail=f"Audio storage failed: {str(e)}")

        # --- Step 3: Transcribe ---
        try:
            asr_result = await transcribe_audio_with_timestamps(temp_file_path)
        except RuntimeError as e:
            raise HTTPException(status_code=500, detail=f"Transcription failed: {str(e)}")

        if not asr_result["text"]:
            raise HTTPException(
                status_code=422,
                detail="Transcription produced no text — audio may be silent or unclear."
            )

        # --- Step 4: Generate SOAP note ---
        try:
            soap_result = await soap_generator.generate(asr_result["text"])
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except RuntimeError as e:
            raise HTTPException(status_code=500, detail=f"SOAP generation failed: {str(e)}")

        # --- Step 5: Return everything tied to one consultation_id ---
        return {
            "consultation_id": consultation_id,
            "audio": audio_data,
            "transcript": asr_result,
            "soap_note": soap_result,
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        # Always clean up the local temp copy — Cloudinary keeps the real one
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)


# --- Individual endpoints kept for testing/debugging each stage separately ---

@app.post("/transcribe")
async def handle_transcription(file: UploadFile = File(...)):
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail=f"Unsupported file type: {ext}")

    temp_file_path = os.path.join(TEMP_DIR, f"{uuid.uuid4().hex}{ext}")
    try:
        size = await _save_upload(file, temp_file_path)
        if size == 0:
            raise HTTPException(status_code=400, detail="Uploaded file is empty.")
        return await transcribe_audio_with_timestamps(temp_file_path)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)


class TranscriptRequest(BaseModel):
    transcript: str

class ICDRequest(BaseModel):
    query: str


@app.post("/generate-soap")
async def handle_soap_generation(request: TranscriptRequest):
    try:
        return await soap_generator.generate(request.transcript)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
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