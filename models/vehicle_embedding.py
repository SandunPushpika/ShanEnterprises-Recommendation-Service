from sqlalchemy import Column, BigInteger
from pgvector.sqlalchemy import Vector

from configs.database import Base


class VehicleEmbedding(Base):
    __tablename__ = "vehicle_embeddings"

    vehicle_id = Column(
        BigInteger,
        primary_key=True
    )

    embedding = Column(
        Vector(384),
        nullable=False
    )