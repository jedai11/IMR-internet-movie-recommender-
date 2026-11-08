import os
import httpx
import json

key = os.getenv("GEMINI_API_KEY", "")
prompt = """You are an expert filmologist and cinematic archivist.
For each of these movies and dramas:
1. Parasite (2019)
2. The Dark Knight (2008)
3. Interstellar (2014)
4. Squid Game (2021)
5. Train to Busan (2016)
6. Crash Landing on You (2019)
7. Everything Everywhere All at Once (2022)

Identify their iconic official theatrical release front page / one-sheet poster.
Provide the direct image URL from TMDb CDN (https://image.tmdb.org/t/p/w500/...) or IMDb Amazon CDN.
Return ONLY valid JSON matching:
{
  "movies": [
    {
      "title": "Parasite",
      "year": 2019,
      "official_poster_url": "https://image.tmdb.org/t/p/w500/...",
      "poster_description": "Family standing on the lawn with black/white censorship bars over eyes"
    }
  ]
}
"""

url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash:generateContent?key={key}"
r = httpx.post(url, json={"contents": [{"parts": [{"text": prompt}]}]}, timeout=15.0)
print("Status:", r.status_code)
print(r.json()["candidates"][0]["content"]["parts"][0]["text"])

