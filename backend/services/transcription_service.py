from backend.asr.asr_service import transcribe_audio_with_timestamps
from backend.diarization.speaker_diarizer import diarize_audio
from backend.diarization.merge_speakers import merge_speakers


SPEAKER_ROLE_MAP = {
    "SPEAKER_0": "Doctor",
    "SPEAKER_1": "Patient"
}


async def process_audio(audio_path: str):

    # 1. ASR
    asr_result = await transcribe_audio_with_timestamps(audio_path)
    asr_segments = asr_result["segments"]

    # 2. DIARIZATION
    speaker_segments = diarize_audio(audio_path)

    # 3. MERGE
    merged = merge_speakers(
        asr_segments,
        speaker_segments,
        SPEAKER_ROLE_MAP
    )

    return {"segments": merged}