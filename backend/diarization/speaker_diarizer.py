import numpy as np
import librosa
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score


def _extract_mfcc_features(y: np.ndarray, sr: int, start: float, end: float) -> np.ndarray:
    start_sample = max(0, int(start * sr))
    end_sample = min(len(y), int(end * sr))

    if end_sample <= start_sample:
        return np.zeros(20)

    clip = y[start_sample:end_sample]

    if len(clip) < sr * 0.05:
        return np.zeros(20)

    mfcc = librosa.feature.mfcc(y=clip, sr=sr, n_mfcc=20)
    return np.mean(mfcc, axis=1)


def _alternate_speakers(segments: list[dict]) -> list[dict]:
    """
    Fallback for audio where the two speakers aren't acoustically distinguishable
    (single voice, TTS, or low-quality recordings). Assumes the dataset follows a
    strict back-and-forth conversational pattern, which holds for most scripted
    consultation transcripts and synthetic Q&A datasets.
    """
    return [
        {**seg, "speaker": "Doctor" if i % 2 == 0 else "Patient"}
        for i, seg in enumerate(segments)
    ]


def diarize_segments(file_path: str, segments: list[dict]) -> list[dict]:
    if not segments:
        return []

    if len(segments) < 4:
        # Too few segments for clustering to be meaningful either way
        return _alternate_speakers(segments)

    y, sr = librosa.load(file_path, sr=16000, mono=True)

    features = np.array([
        _extract_mfcc_features(y, sr, seg["start"], seg["end"])
        for seg in segments
    ])

    if np.allclose(features, features[0]):
        return _alternate_speakers(segments)

    kmeans = KMeans(n_clusters=2, n_init=10, random_state=42)
    cluster_ids = kmeans.fit_predict(features)

    try:
        score = silhouette_score(features, cluster_ids)
    except ValueError:
        score = -1  

    SILHOUETTE_THRESHOLD = 0.15
    if score < SILHOUETTE_THRESHOLD:
        return _alternate_speakers(segments)

    doctor_cluster = cluster_ids[0]
    diarized = []
    for seg, cluster_id in zip(segments, cluster_ids):
        speaker = "Doctor" if cluster_id == doctor_cluster else "Patient"
        diarized.append({**seg, "speaker": speaker})

    return diarized


def diarize_audio() -> dict:
    return {
        "status": "success",
        "note": "Real diarization runs inside /process-consultation via diarize_segments().",
    }