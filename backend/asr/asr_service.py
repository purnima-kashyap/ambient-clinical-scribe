import os
import asyncio
from faster_whisper import WhisperModel

async def transcribe_audio_with_timestamps(file_path: str) -> dict:
    """
    Calls local faster-whisper to transcribe audio and extract segment-level 
    timestamps required for downstream Speaker Diarization.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Audio file not found at: {file_path}")
        
    try:
        def run_transcription():
            
            
            local_model = WhisperModel("small", device="cpu", compute_type="int8")
            
            segments_generator, info = local_model.transcribe(
                file_path,
                beam_size=5,
                initial_prompt="Medical consultation detailing clinical symptoms, patient history, and pharmacology."
            )
            
            segments = []
            full_text = ""
            
            for segment in segments_generator:
                segments.append({
                    "start": segment.start,
                    "end": segment.end,
                    "text": segment.text
                })
                full_text += segment.text + " "
                
            return {
                "text": full_text.strip(),
                "segments": segments,
                "language": info.language
            }
            
        # Run the CPU-heavy task in a background thread
        result = await asyncio.to_thread(run_transcription)
        return result
        
    except Exception as e:
        raise RuntimeError(f"Local ASR failed: {str(e)}")