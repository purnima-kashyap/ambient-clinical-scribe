from backend.asr.asr_service import transcribe_audio_with_timestamps
from backend.diarization.speaker_diarizer import diarize_audio
from backend.diarization.merge_speakers import merge_speakers

from backend.services.role_detector import detect_roles


async def process_audio(audio_path: str):

    # 1. ASR
    asr_result = await transcribe_audio_with_timestamps(audio_path)
    asr_segments = asr_result["segments"]

    # 2. DIARIZATION
    speaker_segments = diarize_audio(audio_path)


    # 3. Merge
    merged = merge_speakers(
        asr_segments,
        speaker_segments
    )

    # 4. Detect Doctor/Patient
    merged = detect_roles(merged)

    return {
    "text": asr_result["text"],
    "language": asr_result["language"],
    "segments": merged,
    }