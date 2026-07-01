from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import uuid
import asyncio

from backend.asr.asr_service import transcribe_audio_with_timestamps
from backend.diarization.speaker_diarizer import diarize_segments, diarize_audio
from backend.storage.cloudinary_service import upload_audio_to_cloudinary
from backend.llm.llm_service import SOAPNoteGenerator
from backend.rag.icd10_recommender import ICD10Recommender

app = FastAPI(title="AI Clinical Scribe API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

soap_generator = SOAPNoteGenerator()
icd10_recommender = ICD10Recommender()

ALLOWED_EXTENSIONS = {".wav", ".mp3", ".m4a", ".webm", ".ogg"}
MAX_FILE_SIZE = 25 * 1024 * 1024  # 25 MB
TEMP_DIR = os.path.join(os.path.dirname(__file__), "..", "temp_uploads")
os.makedirs(TEMP_DIR, exist_ok=True)


@app.get("/")
def home():
    return {"message": "Healthcare AI Scribe Running"}


@app.get("/diarize")
def diarize_stub():
    return diarize_audio()


async def _save_upload(file: UploadFile, temp_file_path: str) -> int:
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
    1. Save audio temporarily -> 2. Upload to Cloudinary -> 3. Transcribe (Whisper)
    -> 4. Diarize (MFCC+KMeans) -> 5. Generate SOAP note -> 6. ICD-10 RAG -> 7. Cleanup
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
        size = await _save_upload(file, temp_file_path)
        if size == 0:
            raise HTTPException(status_code=400, detail="Uploaded file is empty.")

        try:
            audio_data = await upload_audio_to_cloudinary(temp_file_path, public_id=consultation_id)
        except RuntimeError as e:
            raise HTTPException(status_code=502, detail=f"Audio storage failed: {str(e)}")

        try:
            asr_result = await transcribe_audio_with_timestamps(temp_file_path)
        except RuntimeError as e:
            raise HTTPException(status_code=500, detail=f"Transcription failed: {str(e)}")

        if not asr_result["text"]:
            raise HTTPException(
                status_code=422,
                detail="Transcription produced no text — audio may be silent or unclear."
            )

        try:
            diarized_segments = await asyncio.to_thread(
                diarize_segments, temp_file_path, asr_result["segments"]
            )
        except Exception:
            diarized_segments = asr_result["segments"]

        try:
            soap_result = await soap_generator.generate(asr_result["text"])
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except RuntimeError as e:
            raise HTTPException(status_code=500, detail=f"SOAP generation failed: {str(e)}")

        try:
            icd10_suggestions = icd10_recommender.recommend(soap_result.assessment)
        except Exception as e:
            print(f"[ICD10 ERROR] {type(e).__name__}: {e}")
            icd10_suggestions = []

        return {
            "consultation_id": consultation_id,
            "audio": audio_data,
            "transcript": {
                "text": asr_result["text"],
                "language": asr_result["language"],
                "segments": diarized_segments,
            },
            "soap_note": soap_result,
            "icd10_recommendations": icd10_suggestions,
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)


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


@app.post("/generate-soap")
async def handle_soap_generation(request: TranscriptRequest):
    try:
        return await soap_generator.generate(request.transcript)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class AssessmentRequest(BaseModel):
    assessment: str


@app.post("/recommend-icd10")
async def handle_icd10_recommendation(request: AssessmentRequest):
    try:
        return {"icd10_recommendations": icd10_recommender.recommend(request.assessment)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))