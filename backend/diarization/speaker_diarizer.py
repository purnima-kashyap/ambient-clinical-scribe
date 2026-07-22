import os

import soundfile as sf
import torch
from pyannote.audio import Pipeline

pipeline = None


def get_pipeline():
    global pipeline

    if pipeline is None:
        print("Loading diarization model...")

        token = os.getenv("HF_TOKEN")
        print("HF_TOKEN loaded:", token is not None)
        print("HF_TOKEN prefix:", token[:8] if token else None)

        pipeline = Pipeline.from_pretrained(
            "pyannote/speaker-diarization-3.1",
            use_auth_token=os.getenv("HF_TOKEN")
        )

        print("Pipeline loaded!")

    return pipeline


def _load_waveform(file_path):
    # pyannote 4.x decodes file paths through torchcodec, which needs a
    # system FFmpeg (full-shared) build that isn't present here. Preloading
    # the audio in memory and handing pyannote a {"waveform", "sample_rate"}
    # dict bypasses torchcodec entirely; only torchaudio is used, for the
    # internal downmix/resample to 16 kHz.
    data, sample_rate = sf.read(file_path, dtype="float32", always_2d=True)
    # soundfile returns (time, channel); pyannote expects (channel, time).
    waveform = torch.from_numpy(data.T)
    return {"waveform": waveform, "sample_rate": sample_rate}


def diarize_audio(file_path):
    pipeline = get_pipeline()

    diarization = pipeline(
        file_path,
        num_speakers=2
    )

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

    return results

    pipeline = get_pipeline()

    diarization = pipeline(file_path)

    results = []

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

    return results