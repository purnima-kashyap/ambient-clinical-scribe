# Dataset & Testing

This folder contains the datasets and test files used for the Ambient Clinical Scribe project.

## Folder Structure

```
data/
├── audio_samples/
├── transcripts/
├── soap_test_cases/
└── icd10_dataset.csv
```

## Contents

### audio_samples
Contains sample doctor-patient conversation audio files used for Speech-to-Text (Whisper) testing.

### transcripts
Contains manually prepared doctor-patient conversation transcripts.

Example:
- fever_case_01.txt
- diabetes_case_01.txt
- hypertension_case_01.txt

### soap_test_cases
Contains the expected SOAP note output corresponding to each transcript.

Example:
- fever_case_01_expected.txt
- diabetes_case_01_expected.txt
- hypertension_case_01_expected.txt

### icd10_dataset.csv
Contains a reference dataset of ICD-10 codes mapped to common clinical conditions.

## Purpose

These datasets are intended for:

- Speech-to-Text testing
- SOAP note generation testing
- Clinical documentation validation
- ICD-10 code mapping
- AI workflow testing

## Naming Convention

Transcript:

```
condition_case_01.txt
```

SOAP Expected Output:

```
condition_case_01_expected.txt
```

Audio Sample:

```
condition_case_01.wav
```

## Current Clinical Conditions

- Fever
- Common Cold
- Upper Respiratory Infection
- Type 2 Diabetes
- Hypertension
- Migraine
- Asthma
- GERD
- Urinary Tract Infection
- Low Back Pain
- Headache
- Acute Sinusitis
- Acute Otitis Media
- Allergic Rhinitis
- Gastritis
- Viral Gastroenteritis
- Generalized Anxiety Disorder
- Insomnia
- Knee Pain
- Shoulder Pain
- Cervical Spondylosis

## Maintainer

Dataset prepared by Romana Parkar as part of the Dataset & Testing module for the Ambient Clinical Scribe project.