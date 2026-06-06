from sqlalchemy.orm import Session  # type: ignore
from sqlalchemy import text  # type: ignore

from models.vehicle_embedding import VehicleEmbedding


class EmbeddingRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_by_vehicle_id(
        self,
        vehicle_id: int
    ):
        return (
            self.db.query(VehicleEmbedding)
            .filter(
                VehicleEmbedding.vehicle_id == vehicle_id
            )
            .first()
        )

    def insert_embedding(
        self,
        vehicle_id: int,
        embedding: list
    ):
        entity = VehicleEmbedding(
            vehicle_id=vehicle_id,
            embedding=embedding
        )

        self.db.add(entity)
        self.db.commit()

        return entity

    def update_embedding(
        self,
        vehicle_id: int,
        embedding: list
    ):
        entity = self.get_by_vehicle_id(vehicle_id)

        if not entity:
            return None

        entity.embedding = embedding

        self.db.commit()

        return entity

    def upsert_embedding(
        self,
        vehicle_id: int,
        embedding: list
    ):
        existing = self.get_by_vehicle_id(vehicle_id)

        if existing:
            existing.embedding = embedding
            self.db.commit()
            return existing

        entity = VehicleEmbedding(
            vehicle_id=vehicle_id,
            embedding=embedding
        )

        self.db.add(entity)
        self.db.commit()

        return entity

    def delete_embedding(
        self,
        vehicle_id: int
    ):
        entity = self.get_by_vehicle_id(vehicle_id)

        if entity:
            self.db.delete(entity)
            self.db.commit()

    def get_all(self):
        return self.db.query(
            VehicleEmbedding
        ).all()

    def search_similar(
        self,
        query_embedding: list,
        limit: int = 5
    ):
        sql = text("""
            SELECT
                vehicle_id,
                1 - (embedding <=> CAST(:embedding AS vector))
                    AS similarity
            FROM vehicle_embeddings
            ORDER BY similarity DESC
            LIMIT :limit
        """)

        result = self.db.execute(
            sql,
            {
                "embedding": str(query_embedding),
                "limit": limit
            }
        )

        return [
            {
                "vehicle_id": row.vehicle_id,
                "similarity": float(row.similarity)
            }
            for row in result
        ]
