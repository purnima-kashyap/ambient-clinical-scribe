import faiss
import pandas as pd
from sentence_transformers import SentenceTransformer


from backend.vector_db.config import ICD_DATASET_PATH, VECTOR_DB_PATH

class ICD10Recommender:
    def __init__(self, top_k: int = 5):
        """
        Initializes the Semantic RAG Recommender.
        Heavy loading (Neural Network and Database) happens HERE, exactly once.
        """
        self.top_k = top_k
        
        print("Loading HuggingFace Model & FAISS Index... (This will take a few seconds)")
        
        # 1. Load the Dataset
        self.df = pd.read_csv(ICD_DATASET_PATH)
        if not {"code", "description"}.issubset(self.df.columns):
            raise ValueError("Dataset must have 'code' and 'description' columns.")
            
        # 2. Load the Embedding Model
        # This is the 90MB neural network. Loading it here prevents the 2-second lag per request
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        
        # 3. Load the FAISS Index
        self.index = faiss.read_index(str(VECTOR_DB_PATH))
        
        print("✅ Semantic Search Engine Ready!")

    def recommend(self, assessment_text: str) -> list[dict]:
        """
        Converts the doctor's assessment into a vector and searches FAISS.
        """
        if not assessment_text or not assessment_text.strip():
            return []
            
        # 1. Turn the text into mathematical numbers (Semantic Vector)
        query_embedding = self.model.encode([assessment_text])
        
        # 2. Search the FAISS database for the closest vectors
        distances, indices = self.index.search(query_embedding.astype("float32"), self.top_k)
        
        results = []
        for i in range(self.top_k):
            idx = indices[0][i]
            
            # FAISS returns -1 if it can't find enough matches
            if idx == -1: 
                continue
                
            row = self.df.iloc[idx]
            
            # 3. Package the results (fixed the 'disease' vs 'description' bug here)
            results.append({
                "code": row["code"],
                "description": row["description"], 
                "distance": float(distances[0][i]),
                "score": float(distances[0][i]) 
            })
            
        return results