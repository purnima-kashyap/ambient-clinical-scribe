# Dataset Guidelines

This document defines the standard format for all datasets used in the Ambient Clinical Scribe project.

## Transcript Format

Each transcript should contain a natural conversation between a doctor and a patient.

Example:

Doctor: What brings you in today?

Patient: I have had a fever for three days.

Doctor: Any cough?

Patient: Yes, a mild cough.

---

## SOAP Test Case Format

Every transcript must have one corresponding expected SOAP output.

Structure:

Subjective:
...

Objective:
...

Assessment:
...

Plan:
...

---

## ICD-10 Dataset

The ICD-10 dataset must contain two columns.

| code | disease |
|------|----------|
| I10 | Hypertension |
| E11.9 | Type 2 Diabetes |

---

## Naming Convention

Transcript:

condition_case_01.txt

SOAP:

condition_case_01_expected.txt

Audio:

condition_case_01.wav

---

## Folder Structure

data/
├── audio_samples/
├── transcripts/
├── soap_test_cases/
└── icd10_dataset.csv

---

## Future Improvements

- More clinical conditions
- Multiple cases per condition
- Real patient audio samples
- Larger ICD-10 reference dataset