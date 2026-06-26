import faiss
import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer

from config import ICD_DATASET_PATH, VECTOR_DB_PATH


def load_icd_dataset():
    """
    Loads the ICD-10 dataset from the CSV file.
    """
    df = pd.read_csv(ICD_DATASET_PATH)

    return df


def load_embedding_model():
    """
    Loads the Sentence Transformer model.
    """
    model = SentenceTransformer("all-MiniLM-L6-v2")

    return model

def generate_embeddings(model, dataset):
    """
    Converts all disease names into vector embeddings.
    """

    diseases = dataset["disease"].tolist()

    embeddings = model.encode(diseases)

    return embeddings

def build_faiss_index(embeddings):
    """
    Creates a FAISS index from the embeddings.
    """

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(dimension)

    index.add(np.array(embeddings).astype("float32"))

    return index

def save_faiss_index(index):
    """
    Saves the FAISS index to disk.
    """
    VECTOR_DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    faiss.write_index(index, str(VECTOR_DB_PATH))


if __name__ == "__main__":

    dataset = load_icd_dataset()

    print(dataset.head())

    print("\nLoading embedding model...\n")

    model = load_embedding_model()

    print("Embedding model loaded successfully!")

    embeddings = generate_embeddings(model, dataset)

    print("\nEmbedding Shape:", embeddings.shape)

    print("\nFirst Embedding:")

    print(embeddings[0])

    print("\nBuilding FAISS index...\n")

    index = build_faiss_index(embeddings)

    save_faiss_index(index)

    print(f"FAISS index created successfully!")

    print(f"Total vectors stored: {index.ntotal}")