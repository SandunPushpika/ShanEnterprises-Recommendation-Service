from services.embedding_service import (
    VehicleEmbeddingService
)

from repositories.vehicle_embedding_repository import (
    EmbeddingRepository,
)

from repositories.review_repository import (
    ReviewRepository,
)


class VehicleEmbeddingManager:

    def __init__(
        self,
        review_repository: ReviewRepository,
        embedding_repository: EmbeddingRepository,
        embedding_service: VehicleEmbeddingService
    ):
        self.review_repository = review_repository
        self.embedding_repository = embedding_repository
        self.embedding_service = embedding_service

    def update_vehicle_embedding(
        self,
        vehicle_id: int,
        reviews: list[str]
    ):
        embedding = (
            self.embedding_service
            .generate_vehicle_embedding(reviews)
        )

        self.repository.upsert_embedding(
            vehicle_id,
            embedding.tolist()
        )

    def search_vehicles(
        self,
        query: str,
        limit: int = 5
    ):
        query_embedding = (
            self.embedding_service
            .generate_query_embedding(query)
        )

        return self.embedding_repository.search_similar(
            query_embedding.tolist(),
            limit
        )

    def rebuild_vehicle_embedding(
        self,
        vehicle_id: int
    ):
        reviews = (
            self.review_repository
            .get_vehicle_reviews(vehicle_id)
        )

        if not reviews:
            print("No reviews found for vehicle_id:", vehicle_id)
            return

        print(f"Rebuilding embedding for vehicle_id: {vehicle_id} with {len(reviews)} reviews")
        vehicle_embedding = (
            self.embedding_service
            .generate_vehicle_embedding(reviews)
        )
        print(f"Generated embedding for vehicle_id: {vehicle_id}, embedding shape: {vehicle_embedding.shape}")
        
        self.embedding_repository.upsert_embedding(
            vehicle_id,
            vehicle_embedding.tolist()
        )
        print(f"Upserted embedding for vehicle_id: {vehicle_id}")
