from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models import UserRating, MovieTitle
from app.schemas.feedback import FeedbackRequest, FeedbackResponse

router = APIRouter(prefix="/feedback", tags=["feedback"])

@router.post("", response_model=FeedbackResponse)
def submit_feedback(
    request: FeedbackRequest,
    db: Session = Depends(get_db)
):
    """
    Submits 1-tap user feedback on a recommended movie.
    Actions: 'watched', 'helped', 'skipped', 'disliked'
    Used to evolve profile confidence from cold-start to established taste weights.
    """
    # Verify title exists
    movie = db.query(MovieTitle).filter(MovieTitle.id == request.title_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Title not found in catalog")

    rating = UserRating(
        session_id=request.session_id,
        title_id=request.title_id,
        feedback_action=request.feedback_action.lower()
    )
    db.add(rating)
    db.commit()

    return FeedbackResponse(
        success=True,
        message=f"Feedback '{request.feedback_action}' recorded for {movie.title}."
    )

