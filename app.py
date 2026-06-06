from fastapi import FastAPI, BackgroundTasks #type: ignore

from configs.database import SessionLocal
from models.requests import RankRequest, ReviewRequest

from services.embedding_service import VehicleEmbeddingService
from services.vehicle_embedding_service import VehicleEmbeddingManager
from repositories.review_repository import ReviewRepository
from repositories.vehicle_embedding_repository import EmbeddingRepository

app = FastAPI()

embedding_service = VehicleEmbeddingService()


def get_manager():
    db = SessionLocal()

    return VehicleEmbeddingManager(
        review_repository=ReviewRepository(db),
        embedding_repository=EmbeddingRepository(db),
        embedding_service=embedding_service
    )


@app.get("/api/health")
def health():
    return {"status": "running"}


@app.post("/api/review")
def trigger_embedding_update(
    request: ReviewRequest,
    background_tasks: BackgroundTasks
):

    manager = get_manager()

    background_tasks.add_task(
        manager.rebuild_vehicle_embedding,
        request.vehicle_id
    )

    return {
        "message": "Embedding rebuild triggered",
        "vehicle_id": request.vehicle_id
    }

@app.post("/api/vehicles/rank")
def rank_vehicles(request: RankRequest):

    manager = get_manager()

    results = manager.search_vehicles(
        query=request.query,
        limit=request.limit
    )

    return {
        "results": results
    }