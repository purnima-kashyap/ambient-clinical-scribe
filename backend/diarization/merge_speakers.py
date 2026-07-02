
from typing import List, Dict, Any


def overlaps(a_start, a_end, b_start, b_end):
    return a_start < b_end and a_end > b_start


def merge_speakers(
    asr_segments: List[Dict[str, Any]],
    speaker_segments: List[Dict[str, Any]],
    speaker_map: Dict[str, str] = None
) -> List[Dict[str, Any]]:

  

    speaker_map = speaker_map or {}

    merged = []

    for segment in asr_segments:
        speaker_name = "Unknown"

        for speaker in speaker_segments:
            if overlaps(
                segment["start"], segment["end"],
                speaker["start"], speaker["end"]
            ):
                raw_speaker = speaker["speaker"]
                speaker_name = speaker_map.get(raw_speaker, raw_speaker)
                break

        merged.append({
            "speaker": speaker_name,
            "start": segment["start"],
            "end": segment["end"],
            "text": segment["text"]
        })

    return merged