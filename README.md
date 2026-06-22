# ambient-clinical-scribe
AI-powered healthcare scribe and SOAP note generator

This project is an AI-powered healthcare assistant that listens to doctor-patient conversations, converts speech into text, and automatically generates structured medical SOAP notes (Subjective, Objective, Assessment, Plan). It helps reduce doctors' documentation time and improves workflow efficiency.

## backend setup and environment configuration
Created project structure using FastAPI
Set up Python virtual environment (.venv)
Installed required dependencies

Setup & Installation (What I installed)
1. Python Environment Setup : python -m venv .venv
Activate environment: .venv\Scripts\activate

2. Install Core Dependencies : python -m pip install fastapi uvicorn

3. run : uvicorn backend.main:app --reload

## 🔊 Speaker Diarization Module
Implemented the speaker diarization component to distinguish between different speakers in a doctor-patient conversation.

- Identifies multiple speakers in an audio recording.
- Labels speakers (e.g., Doctor and Patient).
- Provides structured output for downstream SOAP note generation.
- Integrated with FastAPI endpoints.

GET `/diarize`
Returns speaker diarization results.

## Audio Transcription Module

This module uses Faster-Whisper to transcribe audio files and extract segment-level timestamps required for downstream speaker diarization.

Use Case:
This module serves as the Automatic Speech Recognition (ASR) component of the AI Medical Scribe pipeline and provides timestamped transcripts for speaker diarization and SOAP note generation.

Features: 
Speech-to-text transcription using Faster-Whisper
Segment-level timestamps
Automatic language detection
Medical-context prompt for improved accuracy
Asynchronous execution using asyncio.to_thread()

Install the required packages:
pip install faster-whisper
pip install python-multipart 

pip install transformers torch accelerate

## AI Clinical SOAP Note Generator
An AI-powered clinical scribe that converts raw doctor-patient conversation transcripts into structured SOAP (Subjective, Objective, Assessment, Plan) notes using LangChain, Ollama, and Llama 3.

Features:
Generates professional SOAP notes from medical transcripts.
Uses a local Llama 3 model through Ollama.
Structured JSON output with Pydantic validation.
Built with LangChain and asynchronous processing.
Prevents hallucinations by extracting only explicitly stated medical information.

Installation
pip install langchain langchain-core langchain-ollama pydantic

Purpose
This project demonstrates how local large language models can be used to automate clinical documentation and improve healthcare workflow efficiency.