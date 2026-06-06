from typing import List
import numpy as np #type: ignore
from sentence_transformers import SentenceTransformer #type: ignore
from sklearn.metrics.pairwise import cosine_similarity #type: ignore


class VehicleEmbeddingService:

    def __init__(self,
                 model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def generate_review_embedding(self, review: str) -> np.ndarray:
        return self.model.encode(
            review,
            convert_to_numpy=True,
            normalize_embeddings=True
        )

    def generate_review_embeddings(
        self,
        reviews: List[str]
    ) -> np.ndarray:
        if not reviews:
            raise ValueError("Review list cannot be empty")

        return self.model.encode(
            reviews,
            convert_to_numpy=True,
            normalize_embeddings=True
        )

    def generate_vehicle_embedding(
        self,
        reviews: List[str]
    ) -> np.ndarray:

        if not reviews:
            raise ValueError("Vehicle must contain reviews")

        review_vectors = self.generate_review_embeddings(reviews)

        vehicle_vector = np.mean(review_vectors, axis=0)

        norm = np.linalg.norm(vehicle_vector)

        if norm > 0:
            vehicle_vector = vehicle_vector / norm

        return vehicle_vector

    def generate_query_embedding(
        self,
        query: str
    ) -> np.ndarray:

        return self.model.encode(
            query,
            convert_to_numpy=True,
            normalize_embeddings=True
        )

    def similarity(
        self,
        query_embedding: np.ndarray,
        vehicle_embedding: np.ndarray
    ) -> float:

        score = cosine_similarity(
            [query_embedding],
            [vehicle_embedding]
        )[0][0]

        return float(score)

    def rank_vehicles(
        self,
        query: str,
        vehicle_embeddings: dict
    ) -> List[dict]:

        query_embedding = self.generate_query_embedding(query)

        results = []

        for vehicle_id, vehicle_embedding in vehicle_embeddings.items():

            score = self.similarity(
                query_embedding,
                vehicle_embedding
            )

            results.append({
                "vehicle_id": vehicle_id,
                "score": round(score, 4)
            })

        results.sort(
            key=lambda x: x["score"],
            reverse=True
        )

        return results