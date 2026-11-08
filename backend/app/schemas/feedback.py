from pydantic import BaseModel, Field

class FeedbackRequest(BaseModel):
    session_id: str
    title_id: str
    feedback_action: str = Field(..., description="'watched', 'helped', 'skipped', 'disliked'")

class FeedbackResponse(BaseModel):
    success: bool = True
    message: str

