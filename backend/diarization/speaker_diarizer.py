import os
from pyannote.audio import Pipeline

pipeline = None

def get_pipeline():
    global pipeline

    if pipeline is None:
        print("Loading diarization model...")

        pipeline = Pipeline.from_pretrained(
            "pyannote/speaker-diarization",
            use_auth_token=os.getenv("HF_TOKEN")
        )

        print("Pipeline loaded!")

    return pipeline


def diarize_audio(file_path):
    pipeline = get_pipeline()

    diarization = pipeline(file_path)

    results = []

    print("\n========== DIARIZATION OUTPUT ==========")

    for turn, _, speaker in diarization.itertracks(yield_label=True):
        print(
            f"Speaker: {speaker} | "
            f"Start: {turn.start:.2f} | "
            f"End: {turn.end:.2f}"
        )

        results.append({
            "speaker": speaker,
            "start": float(turn.start),
            "end": float(turn.end)
        })

    print("========================================\n")

    return results
    pipeline = get_pipeline()

    diarization = pipeline(file_path)

    results = []

    for turn, _, speaker in diarization.itertracks(yield_label=True):
        results.append({
            "speaker": speaker,
            "start": float(turn.start),
            "end": float(turn.end)
        })

    return results