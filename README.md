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