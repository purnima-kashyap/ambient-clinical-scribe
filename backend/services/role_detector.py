def detect_roles(merged_segments):
    speaker_questions = {}

    # Count questions asked by each speaker
    for seg in merged_segments:
        speaker = seg["speaker"]

        if speaker not in speaker_questions:
            speaker_questions[speaker] = 0

        if seg["text"].strip().endswith("?"):
            speaker_questions[speaker] += 1

    # Need exactly two speakers
    if len(speaker_questions) != 2:
        return merged_segments

    # Speaker with more questions is Doctor
    doctor = max(speaker_questions, key=speaker_questions.get)

    # The other speaker is Patient
    patient = [s for s in speaker_questions if s != doctor][0]

    # Rename speakers
    for seg in merged_segments:
        if seg["speaker"] == doctor:
            seg["speaker"] = "Doctor"
        elif seg["speaker"] == patient:
            seg["speaker"] = "Patient"

    return merged_segments


def fix_questions(segments):
    for i in range(len(segments) - 1):
        current = segments[i]
        nxt = segments[i + 1]

        if (
            current["speaker"] == "Patient"
            and current["text"].strip().endswith("?")
            and nxt["speaker"] == "Patient"
            and nxt["text"].strip().lower().startswith(
                ("yes", "no", "i", "my", "only")
            )
        ):
            current["speaker"] = "Doctor"

    return segments