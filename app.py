import os
from fastapi import Depends, FastAPI, BackgroundTasks, HTTPException, Security, status #type: ignore
from fastapi.security import APIKeyHeader #type: ignore

from configs.database import SessionLocal
from models.requests import RankRequest, ReviewRequest

from services.embedding_service import VehicleEmbeddingService
from services.vehicle_embedding_service import VehicleEmbeddingManager
from repositories.review_repository import ReviewRepository
from repositories.vehicle_embedding_repository import EmbeddingRepository

app = FastAPI()

API_KEY_NAME = "X-API-Key"
API_KEY = os.getenv("API_KEY")
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

embedding_service = VehicleEmbeddingService()

def validate_api_key(api_key: str = Security(api_key_header)):
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API Key missing",
            headers={"WWW-Authenticate": API_KEY_NAME},
        )

    if api_key != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key",
            headers={"WWW-Authenticate": API_KEY_NAME},
        )
    
    return api_key

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
    background_tasks: BackgroundTasks,
    _: str = Depends(validate_api_key)
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
def rank_vehicles(request: RankRequest, _: str = Depends(validate_api_key)):

    manager = get_manager()

    results = manager.search_vehicles(
        query=request.query,
        limit=request.limit
    )

    return {
        "results": results
    }