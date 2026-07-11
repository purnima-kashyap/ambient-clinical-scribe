def detect_roles(segments):
    """
    Label each utterance as Doctor or Patient based on its content.
    Works even if diarization mixes speaker IDs.
    """

    doctor_starters = (
        "what",
        "when",
        "where",
        "why",
        "how",
        "how long",
        "since when",
        "do you",
        "did you",
        "are you",
        "have you",
        "can you",
        "could you",
        "would you",
        "will you",
        "tell me",
        "describe",
        "show me",
        "any",
        "is there",
        "does it",
    )

    patient_starters = (
        "yes",
        "no",
        "i",
        "i'm",
        "i’ve",
        "i've",
        "my",
        "me",
        "it hurts",
        "pain",
        "fever",
        "cough",
        "headache",
        "vomiting",
        "around",
        "about",
        "sometimes",
        "never",
        "always",
        "for",
        "since",
    )

    previous_role = None

    for seg in segments:

        text = seg["text"].strip().lower()

        # Doctor question
        if text.endswith("?") or text.startswith(doctor_starters):
            seg["speaker"] = "Doctor"
            previous_role = "Doctor"

        # Patient reply
        elif text.startswith(patient_starters):
            seg["speaker"] = "Patient"
            previous_role = "Patient"

        # Short reply after doctor's question
        elif (
            previous_role == "Doctor"
            and len(text.split()) <= 6
        ):
            seg["speaker"] = "Patient"
            previous_role = "Patient"

        else:
            seg["speaker"] = previous_role or seg["speaker"]

    return segments