from typing import List, Dict, Any


def overlap_duration(a_start, a_end, b_start, b_end):
    return max(0.0, min(a_end, b_end) - max(a_start, b_start))


def merge_speakers(
    asr_segments: List[Dict[str, Any]],
    speaker_segments: List[Dict[str, Any]],
    speaker_map: Dict[str, str] = None,
):

    speaker_map = speaker_map or {}

    merged = []

    for segment in asr_segments:

        best_speaker = "Unknown"
        best_overlap = 0.0

        for speaker in speaker_segments:

            overlap = overlap_duration(
                segment["start"],
                segment["end"],
                speaker["start"],
                speaker["end"],
            )

            if overlap > best_overlap:
                best_overlap = overlap
                raw = speaker["speaker"]
                best_speaker = speaker_map.get(raw, raw)

        merged.append({
            "speaker": best_speaker,
            "start": segment["start"],
            "end": segment["end"],
            "text": segment["text"],
        })

    return merged


def fix_doctor_patient_labels(segments):
    ANSWER_STARTS = (
        "yes",
        "no",
        "i",
        "i'm",
        "i've",
        "my",
        "only"
    )

    for i in range(len(segments) - 1):
        current = segments[i]
        nxt = segments[i + 1]

        current_text = current["text"].strip().lower()
        next_text = nxt["text"].strip().lower()

        if (
            current_text.endswith("?")
            and current["speaker"] == nxt["speaker"]
            and next_text.startswith(ANSWER_STARTS)
        ):
            current["speaker"] = "Doctor"
            nxt["speaker"] = "Patient"

    return segments