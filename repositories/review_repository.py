from sqlalchemy.orm import Session # type: ignore
from models.review import Review


class ReviewRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_vehicle_reviews(
        self,
        vehicle_id: int
    ) -> list[str]:

        reviews = (
            self.db.query(Review.comment)
            .filter(
                Review.vehicle_id == vehicle_id,
                Review.comment.isnot(None)
            )
            .all()
        )

        return [r[0] for r in reviews]