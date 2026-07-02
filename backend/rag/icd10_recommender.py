import os
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

_DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "data", "icd10_dataset.csv")


class ICD10Recommender:
    def __init__(self, csv_path: str = _DATA_PATH, top_k: int = 5):
        self.top_k = top_k
        self.df = pd.read_csv(csv_path)

        if not {"code", "description"}.issubset(self.df.columns):
            raise ValueError("icd10_dataset.csv must have 'code' and 'description' columns.")

        self.vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
        self._description_matrix = self.vectorizer.fit_transform(self.df["description"])

    def recommend(self, assessment_text: str) -> list[dict]:
        if not assessment_text or not assessment_text.strip():
            return []

        query_vector = self.vectorizer.transform([assessment_text])
        similarities = cosine_similarity(query_vector, self._description_matrix)[0]

        ranked_indices = similarities.argsort()[::-1][: self.top_k]

        results = []
        for idx in ranked_indices:
            score = float(similarities[idx])
            if score <= 0:
                continue
            results.append({
                "code": self.df.iloc[idx]["code"],
                "description": self.df.iloc[idx]["description"],
                "confidence": round(score, 2),
            })

        return results