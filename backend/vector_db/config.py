from pathlib import Path

# Project root directory
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Path to the ICD-10 dataset
ICD_DATASET_PATH = PROJECT_ROOT / "data" / "icd10_dataset.csv"

# Folder where the FAISS index will be saved
VECTOR_DB_PATH = PROJECT_ROOT / "backend" / "vector_db" / "index" / "faiss_index.bin"