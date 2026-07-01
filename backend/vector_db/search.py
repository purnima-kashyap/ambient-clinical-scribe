import faiss
import pandas as pd
from sentence_transformers import SentenceTransformer

from .config import ICD_DATASET_PATH, VECTOR_DB_PATH


def load_faiss_index():
    """
    Load the saved FAISS index.
    """
    index = faiss.read_index(str(VECTOR_DB_PATH))
    return index


def load_dataset():
    """
    Load the ICD dataset.
    """
    dataset = pd.read_csv(ICD_DATASET_PATH)
    return dataset


def load_embedding_model():
    """
    Load the Sentence Transformer model.
    """
    model = SentenceTransformer("all-MiniLM-L6-v2")
    return model


def search_icd(query, top_k=5):
    """
    Search the FAISS index for the most similar ICD diseases.
    """

    index = load_faiss_index()

    dataset = load_dataset()

    model = load_embedding_model()

    query_embedding = model.encode([query])

    distances, indices = index.search(query_embedding.astype("float32"), top_k)

    results = []

    for i in range(top_k):

        row = dataset.iloc[indices[0][i]]

        results.append(
            {
                "code": row["code"],
                "disease": row["disease"],
                "distance": float(distances[0][i])
            }
        )

    return results

if __name__ == "__main__":

    query = "fever headache cough"

    results = search_icd(query)

    print("\nTop ICD Recommendations:\n")

    for result in results:
        print(result)