import os
from pyannote.audio import Pipeline

print("Loading pipeline...")

pipeline = Pipeline.from_pretrained(
    "pyannote/speaker-diarization",
    use_auth_token=os.getenv("HF_TOKEN")
)

print("Pipeline loaded successfully!")