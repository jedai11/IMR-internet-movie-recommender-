import os
import json
import logging
import subprocess
import urllib.parse
from typing import Optional, Dict, Any, List
import httpx
from app.core.config import settings

logger = logging.getLogger(__name__)

POSTER_CACHE_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "poster_cache"
)
os.makedirs(POSTER_CACHE_DIR, exist_ok=True)


class TMDBService:
    def __init__(self):
        self.api_key = settings.TMDB_API_KEY or "554ae6544a5de71241de6bb3c8d7b96a"
        self.base_url = "https://api.themoviedb.org/3"
        self.image_base = settings.TMDB_IMAGE_BASE_URL.rstrip("/")
        self._memory_cache: Dict[str, Any] = {}

    def _execute_api_request(self, endpoint: str, params: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Executes TMDB API request with httpx and automatic fallback to curl.exe
        to bypass Windows socket resets / TLS handshake drops.
        """
        req_params = dict(params)
        req_params["api_key"] = self.api_key
        url = f"{self.base_url}/{endpoint.lstrip('/')}"

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "application/json"
        }

        # 1. Attempt with HTTPX
        try:
            with httpx.Client(timeout=8.0, headers=headers, follow_redirects=True) as client:
                r = client.get(url, params=req_params)
                if r.status_code == 200:
                    return r.json()
        except Exception as e:
            logger.debug(f"HTTPX request failed ({e}), attempting curl fallback for {url}")

        # 2. Resilient fallback to curl.exe
        try:
            query_str = urllib.parse.urlencode(req_params)
            full_url = f"{url}?{query_str}"
            res = subprocess.run(
                ["curl.exe", "-sSL", "--max-time", "8", full_url],
                capture_output=True,
                text=True,
                encoding="utf-8"
            )
            if res.returncode == 0 and res.stdout.strip():
                return json.loads(res.stdout)
        except Exception as e:
            logger.error(f"Curl fallback failed for {url}: {e}")

        return None

    def search_movie_or_tv(self, title: str, year: Optional[int] = None) -> Optional[Dict[str, Any]]:
        """
        Searches TMDB for a movie or TV show. Checks movies first, then TV / multi.
        """
        cache_key = f"search_{title.lower()}_{year}"
        if cache_key in self._memory_cache:
            return self._memory_cache[cache_key]

        # 1. Search movie
        movie_params: Dict[str, Any] = {"query": title}
        if year:
            movie_params["year"] = year
        data = self._execute_api_request("search/movie", movie_params)

        if data and data.get("results"):
            best = data["results"][0]
            self._memory_cache[cache_key] = {"media_type": "movie", **best}
            return self._memory_cache[cache_key]

        # 2. Search TV shows (e.g., Squid Game, Crash Landing on You, Alice in Borderland)
        tv_params: Dict[str, Any] = {"query": title}
        if year:
            tv_params["first_air_date_year"] = year
        data = self._execute_api_request("search/tv", tv_params)

        if data and data.get("results"):
            best = data["results"][0]
            self._memory_cache[cache_key] = {"media_type": "tv", **best}
            return self._memory_cache[cache_key]

        # 3. Multi-search fallback
        data = self._execute_api_request("search/multi", {"query": title})
        if data and data.get("results"):
            valid = [r for r in data["results"] if r.get("media_type") in ("movie", "tv")]
            if valid:
                best = valid[0]
                self._memory_cache[cache_key] = best
                return best

        return None

    def get_details(self, tmdb_id: int, media_type: str = "movie") -> Optional[Dict[str, Any]]:
        """
        Fetches full details including videos (trailers) and cast.
        """
        cache_key = f"details_{media_type}_{tmdb_id}"
        if cache_key in self._memory_cache:
            return self._memory_cache[cache_key]

        endpoint = f"{media_type}/{tmdb_id}"
        data = self._execute_api_request(endpoint, {"append_to_response": "videos,credits"})
        if not data:
            return None

        # Extract trailer
        trailer_url = None
        for v in data.get("videos", {}).get("results", []):
            if v.get("site") == "YouTube" and v.get("type") in ("Trailer", "Teaser"):
                trailer_url = f"https://www.youtube.com/watch?v={v.get('key')}"
                break

        # Extract top cast & director
        cast = [c.get("name") for c in data.get("credits", {}).get("cast", [])[:5] if c.get("name")]
        directors = [
            c.get("name") for c in data.get("credits", {}).get("crew", [])
            if c.get("job") == "Director" and c.get("name")
        ]

        backdrop_path = data.get("backdrop_path")
        poster_path = data.get("poster_path")

        result = {
            "tmdb_id": tmdb_id,
            "media_type": media_type,
            "title": data.get("title") or data.get("name"),
            "tagline": data.get("tagline") or "",
            "overview": data.get("overview") or "",
            "vote_average": round(float(data.get("vote_average", 0.0)), 1) if data.get("vote_average") else None,
            "vote_count": data.get("vote_count", 0),
            "poster_path": poster_path,
            "poster_url": f"{self.image_base}/w780{poster_path}" if poster_path else None,
            "backdrop_url": f"{self.image_base}/w1280{backdrop_path}" if backdrop_path else None,
            "trailer_url": trailer_url,
            "cast": cast,
            "director": directors[0] if directors else None
        }
        self._memory_cache[cache_key] = result
        return result

    def fetch_and_cache_poster(
        self,
        title: str,
        release_year: Optional[int] = None,
        title_id: Optional[str] = None
    ) -> Optional[str]:
        """
        Ensures a movie poster is available locally in POSTER_CACHE_DIR.
        If not, downloads it from TMDB and caches it.
        Returns the absolute local path if successful.
        """
        target_filename = f"{title_id}.jpg" if title_id else f"{title.lower().replace(' ', '_')}.jpg"
        cached_path = os.path.join(POSTER_CACHE_DIR, target_filename)

        if os.path.exists(cached_path) and os.path.getsize(cached_path) > 1000:
            return cached_path

        # Search TMDB
        match = self.search_movie_or_tv(title, release_year)
        if not match or not match.get("poster_path"):
            return None

        poster_path = match["poster_path"]
        img_url = f"{self.image_base}/w780{poster_path}"

        # Download and write image
        try:
            # First try curl for resilient download
            res = subprocess.run(
                ["curl.exe", "-sSL", "--max-time", "12", img_url, "-o", cached_path],
                capture_output=True
            )
            if res.returncode == 0 and os.path.exists(cached_path) and os.path.getsize(cached_path) > 1000:
                logger.info(f"Cached TMDB poster for '{title}' -> {cached_path}")
                return cached_path
        except Exception as e:
            logger.debug(f"Curl download failed for {img_url}: {e}")

        try:
            with httpx.Client(timeout=10.0, follow_redirects=True) as client:
                resp = client.get(img_url)
                if resp.status_code == 200 and len(resp.content) > 1000:
                    with open(cached_path, "wb") as f:
                        f.write(resp.content)
                    return cached_path
        except Exception as e:
            logger.error(f"HTTPX download failed for {img_url}: {e}")

        return None

    def enrich_movie(self, title: str, year: Optional[int] = None) -> Dict[str, Any]:
        """
        Enriches a movie with TMDB rating, backdrop, trailer, tagline, and details.
        """
        match = self.search_movie_or_tv(title, year)
        if not match or not match.get("id"):
            return {}

        details = self.get_details(match["id"], match.get("media_type", "movie"))
        return details or {}


tmdb_service = TMDBService()
