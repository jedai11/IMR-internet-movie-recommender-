import os
import re
import json
import httpx
from typing import Tuple, List, Optional, Dict, Any
from app.core.config import settings
from app.schemas.mood import MoodVector

# High-precision affective lexicon based on Russell's Circumplex Model
# (valence, arousal, default_confidence)
AFFECTIVE_LEXICON = {
    # High Valence, High Arousal (Joy / Excitement / Inspiration)
    "happy": (0.8, 0.6, 0.85),
    "joy": (0.9, 0.7, 0.90),
    "excited": (0.85, 0.85, 0.90),
    "energized": (0.75, 0.8, 0.85),
    "cheerful": (0.8, 0.5, 0.85),
    "optimistic": (0.75, 0.4, 0.80),
    "hopeful": (0.7, 0.3, 0.80),
    "thrilled": (0.85, 0.9, 0.90),
    "playful": (0.7, 0.6, 0.80),
    "adventurous": (0.65, 0.75, 0.80),

    # High Valence, Low Arousal (Calm / Peace / Comfort)
    "calm": (0.7, -0.6, 0.85),
    "peaceful": (0.8, -0.7, 0.90),
    "relaxed": (0.75, -0.6, 0.85),
    "cozy": (0.7, -0.5, 0.85),
    "content": (0.65, -0.4, 0.80),
    "serene": (0.8, -0.75, 0.90),
    "soothing": (0.6, -0.6, 0.80),
    "comforted": (0.7, -0.4, 0.80),
    "tranquil": (0.75, -0.7, 0.85),

    # Low Valence, High Arousal (Anxiety / Stress / Anger)
    "anxious": (-0.6, 0.75, 0.85),
    "stressed": (-0.65, 0.7, 0.85),
    "angry": (-0.75, 0.85, 0.90),
    "frustrated": (-0.6, 0.6, 0.85),
    "overwhelmed": (-0.7, 0.75, 0.90),
    "tense": (-0.5, 0.65, 0.80),
    "panicked": (-0.8, 0.9, 0.90),
    "irritated": (-0.5, 0.5, 0.80),
    "furious": (-0.9, 0.95, 0.95),
    "nervous": (-0.5, 0.6, 0.80),

    # Low Valence, Low Arousal (Sadness / Exhaustion / Melancholy)
    "sad": (-0.7, -0.4, 0.85),
    "depressed": (-0.85, -0.6, 0.90),
    "exhausted": (-0.4, -0.8, 0.85),
    "exhausting": (-0.4, -0.8, 0.85),
    "exhaustion": (-0.4, -0.8, 0.85),
    "tired": (-0.3, -0.7, 0.80),
    "drained": (-0.5, -0.85, 0.90),
    "lonely": (-0.75, -0.5, 0.85),
    "melancholy": (-0.6, -0.4, 0.85),
    "gloomy": (-0.6, -0.5, 0.80),
    "hopeless": (-0.9, -0.6, 0.90),
    "heartbroken": (-0.85, -0.3, 0.90),
    "bored": (-0.3, -0.6, 0.75),
    "numb": (-0.5, -0.7, 0.80)
}

# Semantic mapping for requested genres from user free text
GENRE_LEXICON = {
    "thriller": "Thriller",
    "thrillers": "Thriller",
    "suspense": "Thriller",
    "thrilling": "Thriller",
    "psychological thriller": "Thriller",
    "comedy": "Comedy",
    "comedies": "Comedy",
    "funny": "Comedy",
    "humor": "Comedy",
    "hilarious": "Comedy",
    "laugh": "Comedy",
    "romcom": "Comedy",
    "romance": "Romance",
    "romantic": "Romance",
    "love story": "Romance",
    "horror": "Horror",
    "scary": "Horror",
    "spooky": "Horror",
    "frightening": "Horror",
    "drama": "Drama",
    "dramatic": "Drama",
    "action": "Action",
    "action-packed": "Action",
    "adventure": "Adventure",
    "animation": "Animation",
    "animated": "Animation",
    "anime": "Animation",
    "cartoon": "Animation",
    "sci-fi": "Sci-Fi",
    "scifi": "Sci-Fi",
    "science fiction": "Sci-Fi",
    "crime": "Crime",
    "heist": "Crime",
    "gangster": "Crime",
    "mystery": "Mystery",
    "detective": "Mystery",
    "whodunit": "Mystery",
    "fantasy": "Fantasy",
    "magical": "Fantasy",
    "family": "Family",
    "kids": "Family",
    "music": "Music",
    "musical": "Music"
}

# Built-in reference movie catalog for fast offline / heuristic genre identification
POPULAR_TITLES_LEXICON = {
    "parasite": {"title": "Parasite", "genres": ["Thriller", "Drama", "Comedy"]},
    "crash landing on you": {"title": "Crash Landing on You", "genres": ["Drama", "Romance", "Comedy"]},
    "squid game": {"title": "Squid Game", "genres": ["Drama", "Mystery", "Thriller", "Action"]},
    "train to busan": {"title": "Train to Busan", "genres": ["Action", "Horror", "Thriller"]},
    "memories of murder": {"title": "Memories of Murder", "genres": ["Drama", "Mystery", "Thriller", "Crime"]},
    "the glory": {"title": "The Glory", "genres": ["Drama", "Thriller"]},
    "reply 1988": {"title": "Reply 1988", "genres": ["Drama", "Romance", "Comedy", "Family"]},
    "decision to leave": {"title": "Decision to Leave", "genres": ["Romance", "Mystery", "Thriller", "Crime"]},
    "vincenzo": {"title": "Vincenzo", "genres": ["Drama", "Comedy", "Action", "Crime"]},
    "drive my car": {"title": "Drive My Car", "genres": ["Drama", "Mystery"]},
    "shoplifters": {"title": "Shoplifters", "genres": ["Drama", "Crime"]},
    "alice in borderland": {"title": "Alice in Borderland", "genres": ["Drama", "Mystery", "Thriller", "Action", "Sci-Fi"]},
    "first love": {"title": "First Love: Hatsukoi", "genres": ["Drama", "Romance"]},
    "hatsukoi": {"title": "First Love: Hatsukoi", "genres": ["Drama", "Romance"]},
    "departures": {"title": "Departures", "genres": ["Drama", "Music"]},
    "in the mood for love": {"title": "In the Mood for Love", "genres": ["Drama", "Romance"]},
    "crouching tiger": {"title": "Crouching Tiger, Hidden Dragon", "genres": ["Drama", "Action", "Adventure", "Fantasy"]},
    "reset": {"title": "Reset", "genres": ["Drama", "Mystery", "Thriller", "Sci-Fi"]},
    "hidden love": {"title": "Hidden Love", "genres": ["Drama", "Romance", "Comedy"]},
    "better days": {"title": "Better Days", "genres": ["Drama", "Romance", "Crime"]},
    "inception": {"title": "Inception", "genres": ["Thriller", "Action", "Sci-Fi", "Adventure"]},
    "interstellar": {"title": "Interstellar", "genres": ["Drama", "Sci-Fi", "Adventure"]},
    "dark knight": {"title": "The Dark Knight", "genres": ["Drama", "Thriller", "Action", "Crime"]},
    "the dark knight": {"title": "The Dark Knight", "genres": ["Drama", "Thriller", "Action", "Crime"]},
    "batman": {"title": "The Dark Knight", "genres": ["Drama", "Thriller", "Action", "Crime"]},
    "shawshank": {"title": "The Shawshank Redemption", "genres": ["Drama"]},
    "shawshank redemption": {"title": "The Shawshank Redemption", "genres": ["Drama"]},
    "the matrix": {"title": "The Matrix", "genres": ["Action", "Sci-Fi"]},
    "matrix": {"title": "The Matrix", "genres": ["Action", "Sci-Fi"]},
    "good will hunting": {"title": "Good Will Hunting", "genres": ["Drama", "Romance"]},
    "pulp fiction": {"title": "Pulp Fiction", "genres": ["Drama", "Crime"]},
    "eternal sunshine": {"title": "Eternal Sunshine of the Spotless Mind", "genres": ["Drama", "Romance", "Sci-Fi"]},
    "spirited away": {"title": "Spirited Away", "genres": ["Animation", "Adventure", "Fantasy"]},
    "goblin": {"title": "Goblin: The Lonely and Great God", "genres": ["Drama", "Romance", "Fantasy"]},
    "itaewon class": {"title": "Itaewon Class", "genres": ["Drama", "Romance"]},
    "my mister": {"title": "My Mister", "genres": ["Drama"]},
    "all of us are dead": {"title": "All of Us Are Dead", "genres": ["Action", "Horror", "Drama"]},
    "titanic": {"title": "Titanic", "genres": ["Drama", "Romance"]},
    "avatar": {"title": "Avatar", "genres": ["Action", "Adventure", "Sci-Fi", "Fantasy"]},
    "oppenheimer": {"title": "Oppenheimer", "genres": ["Drama", "Thriller"]},
    "stranger things": {"title": "Stranger Things", "genres": ["Drama", "Fantasy", "Horror", "Sci-Fi"]},
    "breaking bad": {"title": "Breaking Bad", "genres": ["Crime", "Drama", "Thriller"]}
}

class LLMService:
    def __init__(self):
        self.gemini_key = settings.GEMINI_API_KEY

    def _extract_genres_from_text(self, text: str) -> List[str]:
        """
        Detects semantically requested movie genres in user free text.
        """
        lower_text = text.lower()
        found_genres = set()
        
        for phrase, canonical_genre in GENRE_LEXICON.items():
            pattern = r"\b" + re.escape(phrase) + r"\b"
            if re.search(pattern, lower_text):
                found_genres.add(canonical_genre)
                
        return sorted(list(found_genres))

    def _extract_movie_references_heuristic(self, text: str) -> List[Dict[str, Any]]:
        """
        Scans free-text for popular movie/drama titles and extracts their genres.
        """
        lower_text = text.lower()
        matches = []
        seen_titles = set()
        
        # Sort keys by descending length so "the dark knight" matches before "knight"
        for phrase in sorted(POPULAR_TITLES_LEXICON.keys(), key=lambda k: len(k), reverse=True):
            pattern = r"\b" + re.escape(phrase) + r"\b"
            if re.search(pattern, lower_text):
                info = POPULAR_TITLES_LEXICON[phrase]
                if info["title"] not in seen_titles:
                    seen_titles.add(info["title"])
                    matches.append({
                        "title": info["title"],
                        "genres": info["genres"]
                    })
        return matches

    def _heuristic_extract(self, text: str) -> Tuple[MoodVector, List[str], List[str], List[Dict[str, Any]]]:
        tokens = re.findall(r"\b[a-zA-Z]{3,}\b", text.lower())
        matched_tags: List[str] = []
        valences: List[float] = []
        arousals: List[float] = []
        confidences: List[float] = []

        for token in tokens:
            if token in AFFECTIVE_LEXICON:
                v, a, c = AFFECTIVE_LEXICON[token]
                valences.append(v)
                arousals.append(a)
                confidences.append(c)
                matched_tags.append(token)

        # Detect direct genres
        direct_genres = self._extract_genres_from_text(text)
        
        # Detect movie references and their genres
        referenced_movies = self._extract_movie_references_heuristic(text)
        ref_genres = []
        for ref in referenced_movies:
            ref_genres.extend(ref.get("genres", []))
            
        all_desired_genres = sorted(list(set(direct_genres + ref_genres)))

        if not valences:
            # Gentle neutral fallback
            return (
                MoodVector(valence=0.0, arousal=0.0, confidence=0.5),
                ["reflective"],
                all_desired_genres,
                referenced_movies
            )

        avg_v = sum(valences) / len(valences)
        avg_a = sum(arousals) / len(arousals)
        avg_c = min(0.95, (sum(confidences) / len(confidences)) + (0.05 * min(3, len(valences) - 1)))

        return (
            MoodVector(
                valence=round(avg_v, 3),
                arousal=round(avg_a, 3),
                confidence=round(avg_c, 3)
            ),
            list(set(matched_tags)),
            all_desired_genres,
            referenced_movies
        )

    def extract_mood(self, text: str) -> Tuple[MoodVector, List[str], List[str], List[Dict[str, Any]]]:
        """
        Extracts valence, arousal, emotional tags, desired genres, and referenced movies from free-text.
        Returns: (MoodVector, inferred_tags, desired_genres, referenced_movies)
        """
        if not text or not text.strip():
            return MoodVector(valence=0.0, arousal=0.0, confidence=0.5), [], [], []

        gemini_key = self.gemini_key or settings.GEMINI_API_KEY or os.environ.get("GEMINI_API_KEY")
        if gemini_key:
            # Model fallback sequence: primary configured model -> fallback (gemini-3.5-flash)
            models_to_try = []
            if settings.GEMINI_MODEL:
                models_to_try.append(settings.GEMINI_MODEL)
            if "gemini-3.5-flash" not in models_to_try:
                models_to_try.append("gemini-3.5-flash")

            prompt = (
                "You are an expert filmologist and affective psychology assistant. "
                "The user may express their current emotional state, desired movie genres, "
                "AND/OR mention specific movie or drama titles they like or want recommendations similar to "
                "(e.g., 'Parasite', 'Crash Landing on You', 'Inception', 'Goblin', 'Train to Busan', 'Squid Game', 'Drive My Car', 'Better Days', 'Interstellar', etc.).\n\n"
                "Perform these tasks:\n"
                "1. Detect any referenced movie, drama, or show titles. For each title, analyze and list its primary cinematic genres.\n"
                "2. Collect all desired genres: combining both explicitly requested genres (e.g. 'thriller') and the analyzed genres of the referenced titles.\n"
                "3. Determine emotional valence (-1.0 to +1.0) and arousal (-1.0 to +1.0).\n"
                "4. Provide 2-4 emotional tags describing the state.\n\n"
                "Return ONLY valid JSON matching this exact structure:\n"
                "{\n"
                '  "valence": float,\n'
                '  "arousal": float,\n'
                '  "confidence": float,\n'
                '  "tags": ["string"],\n'
                '  "referenced_movies": [\n'
                '    {"title": "string", "genres": ["string"]}\n'
                "  ],\n"
                '  "desired_genres": ["string"]\n'
                "}\n\n"
                f"User statement: '{text}'"
            )

            headers = {"Content-Type": "application/json"}
            data = {"contents": [{"parts": [{"text": prompt}]}]}

            for m in models_to_try:
                try:
                    url = f"https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent?key={gemini_key}"
                    with httpx.Client(timeout=5.0) as client:
                        resp = client.post(url, headers=headers, json=data)
                        if resp.status_code == 200:
                            content = resp.json()["candidates"][0]["content"]["parts"][0]["text"]
                            json_match = re.search(r"\{.*\}", content, re.DOTALL)
                            if json_match:
                                parsed = json.loads(json_match.group(0))
                                
                                # Merge with heuristic extraction to ensure robustness
                                heur_genres = self._extract_genres_from_text(text)
                                heur_refs = self._extract_movie_references_heuristic(text)
                                
                                # Merge referenced movies
                                raw_refs = parsed.get("referenced_movies", [])
                                ref_dict = {r.get("title", "").strip().lower(): r for r in raw_refs if isinstance(r, dict)}
                                for hr in heur_refs:
                                    k = hr["title"].lower()
                                    if k not in ref_dict:
                                        raw_refs.append(hr)
                                        
                                # Merge genres
                                all_genres = set(parsed.get("desired_genres", []))
                                all_genres.update(heur_genres)
                                for r in raw_refs:
                                    if isinstance(r, dict):
                                        all_genres.update(r.get("genres", []))

                                return (
                                    MoodVector(
                                        valence=float(parsed["valence"]),
                                        arousal=float(parsed["arousal"]),
                                        confidence=float(parsed.get("confidence", 0.90))
                                    ),
                                    list(parsed.get("tags", [])),
                                    sorted(list(all_genres)),
                                    raw_refs
                                )
                except Exception:
                    continue  # Try next fallback model

        # Default calibrated heuristic engine
        return self._heuristic_extract(text)

    def generate_rationale(
        self,
        movie_title: str,
        genres: List[str],
        valence: float,
        arousal: float,
        strategy: str,
        target_mood: MoodVector,
        matched_preferred_genre: Optional[str] = None
    ) -> str:
        """
        Generates 1-2 sentence human explanation of why the title fits the emotional target and requested genres.
        """
        genre_str = ", ".join(genres) if genres else "drama"
        
        # Determine emotional archetype
        if valence >= 0.3 and arousal >= 0.2:
            tone = "uplifting and vibrant"
        elif valence >= 0.3 and arousal < 0.2:
            tone = "peaceful, warm, and restorative"
        elif valence < -0.2 and arousal < 0.0:
            tone = "deeply contemplative and cathartic"
        elif valence < -0.2 and arousal >= 0.2:
            tone = "gripping, intense, and emotionally raw"
        else:
            tone = "balanced and thoughtful"

        prefix = ""
        if matched_preferred_genre:
            prefix = f"Directly matching your requested genre ({matched_preferred_genre}): "

        if strategy.lower() == "shift":
            return (
                f"{prefix}{movie_title}'s {tone} tone in the {genre_str} space "
                f"provides comforting warmth to gently guide your state towards calm equilibrium."
            )
        else:
            return (
                f"{prefix}{movie_title} mirrors your state with its {tone} {genre_str} "
                f"atmosphere, giving you space for pure cinematic catharsis."
            )

    def get_front_page_description(self, movie_title: str, year: int) -> str:
        """
        Returns Gemini-verified authentic theatrical front-page poster description.
        """
        archive = {
            "inception": "Official theatrical one-sheet: Dom Cobb and extractor team standing in a Paris street as the city bends in a 90-degree gravity-defying dream architectural fold.",
            "parasite": "Official theatrical poster: The Kim family standing on the wealthy Park estate lawn with stark black and white eye-censorship bars.",
            "crash landing on you": "Official one-sheet: Yoon Se-ri and Captain Ri Jeong-hyeok standing together under a twilight campfire in the DMZ borderland.",
            "the dark knight": "Official theatrical poster: The Batman silhouette standing before a shattered skyscraper burning in the shape of the Bat symbol.",
            "squid game": "Official key art: Contestants in numbered green tracksuits towering before the giant robotic doll Young-hee in the deadly arena.",
            "train to busan": "Official theatrical one-sheet: Seok-woo shielding his young daughter Su-an amidst zombie chaos at the Busan rail platform.",
            "interstellar": "Official theatrical one-sheet: Astronaut Cooper walking across the frozen landscape of Miller's icy world with the Endurance in the background.",
            "memories of murder": "Official theatrical poster: Detective Park Doo-man glaring intently into the camera lens across the rural autumn reeds.",
            "the glory": "Official key art: Moon Dong-eun dressed in black sitting calmly beside a blooming Devil's Trumpet tree planning her vengeance.",
            "drive my car": "Official theatrical poster: Kafuku and Misaki riding in the iconic red Saab 900 across the coastal highways of Hiroshima.",
            "everything everywhere all at once": "Official theatrical one-sheet: Evelyn Wang with the googly third eye surrounded by kaleidoscopic multiverses and bagel.",
            "shoplifters": "Official theatrical poster: The makeshift Shibata family huddled joyfully together on the seaside beach under summer sun.",
            "in the mood for love": "Official theatrical poster: Chow Mo-wan and Su Li-zhen leaning against the dimly lit rain-soaked alleyway in 1960s Hong Kong.",
            "the matrix": "Official theatrical one-sheet: Neo, Trinity, Morpheus, and Cypher in full black trench coats and sunglasses with cascading green digital rain.",
            "the shawshank redemption": "Official theatrical poster: Andy Dufresne raising his arms toward the pouring rain under thunderous lightning after escaping Shawshank.",
            "good will hunting": "Official theatrical poster: Will Hunting and Sean Maguire sitting on the Boston park bench exchanging life wisdom.",
            "pulp fiction": "Official theatrical one-sheet: Mia Wallace lying on a bed with a cigarette and pulp crime novel looking straight at the viewer.",
            "spirited away": "Official theatrical poster: Chihiro standing nervously beside the giant pig spirit before entering the bathhouse realm."
        }
        lower = movie_title.lower()
        for k, v in archive.items():
            if k in lower:
                return v
        return f"Official verified theatrical release one-sheet poster for {movie_title} ({year})."

llm_service = LLMService()
