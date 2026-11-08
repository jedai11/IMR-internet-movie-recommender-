import re
from typing import Tuple, Optional
from app.core.config import settings
from app.schemas.mood import DistressResponse, DistressResource

class DistressSafeguard:
    """
    Early Distress Safeguard Engine.
    Detects acute distress, crisis, or self-harm ideation before candidate retrieval.
    """
    def __init__(self):
        # Base keywords
        patterns = [re.escape(kw) for kw in settings.DISTRESS_KEYWORDS]
        # Contextual regexes for variations
        patterns.extend([
            r"\bi\s*(?:just\s*)?(?:want|wanna|feel\s+like)\s*(?:to\s*)?die\b",
            r"\b(?:kill|killing|end|ending)\s*(?:my\s*(?:own\s*)?life|myself)\b",
            r"\bbetter\s*off\s*dead\b",
            r"\bno\s*reason\s*to\s*live\b",
            r"\bcan'?t\s*(?:go\s*on|take\s*(?:it|this))\s*anymore\b",
            r"\bplease\s*help\s*me\s*end\s*it\b",
            r"\b(?:hurt|hurting|cut|cutting)\s*myself\b",
            r"\bself[\s\-]harm\b",
            r"\boverdose\s*(?:on\s*pills)?\b",
            r"\bdon'?t\s*want\s*to\s*wake\s*up\b"
        ])
        self.regex = re.compile("|".join(patterns), re.IGNORECASE)

    def evaluate(self, text: Optional[str]) -> Tuple[bool, Optional[DistressResponse]]:
        if not text or not text.strip():
            return False, None
        
        normalized = text.strip()
        match = self.regex.search(normalized)
        
        if match:
            helplines = [
                DistressResource(
                    name=hl["name"],
                    contact=hl["contact"],
                    url=hl.get("url")
                ) for hl in settings.SUPPORT_HELPLINES
            ]
            response = DistressResponse(
                distress_detected=True,
                message=(
                    "It sounds like you are going through an overwhelming or painful moment. "
                    "You don't have to carry this alone. Free, confidential support is available 24/7."
                ),
                helplines=helplines,
                gentle_content_option={
                    "title": "Gentle Nature & Calming Spaces",
                    "description": "If you need a quiet, low-stress screen presence, we can suggest serene ambient or comforting nature documentaries.",
                    "recommended_genre": "Documentary"
                }
            )
            return True, response
            
        return False, None

distress_safeguard = DistressSafeguard()
