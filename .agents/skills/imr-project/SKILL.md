---
name: imr-project
description: >-
  Expert knowledge base for the IMR (Internet Movie Recommender / MoodReel) project.
  Activates automatically when working in D:\IMR-Forked. Covers architecture,
  dev workflows, git rules, testing, known bugs, and all file locations so the
  agent can work without asking for context every session.
---

# IMR — Internet Movie Recommender (MoodReel) Project Skill

> [!IMPORTANT]
> This skill must be activated before making ANY change to this project.
> Read every section below before writing a single line of code.

---

## 1. Project Identity

| Field | Value |
|---|---|
| **App name** | MoodReel |
| **Repo root** | `D:\IMR-Forked` |
| **GitHub remote** | `https://github.com/jedai11/IMR-internet-movie-recommender-.git` |
| **Active branch** | `IMR-forked` |
| **Stack** | FastAPI (Python 3.11) + React 18 / TypeScript (Vite) + SQLite (SQLAlchemy) |
| **External API** | TMDB (The Movie Database) — API key in `backend/.env` |
| **AI backend** | Gemini (for mood analysis) — key in `backend/.env` |

---

## 2. Absolute Git Rules

> [!CAUTION]
> **NEVER push to `main`.** The `main` branch is frozen. ALL commits go to `IMR-forked` only.

```powershell
# Always verify branch before commit
git branch   # must show * IMR-forked

# Standard commit flow
git add .
git commit -m "type: description"
git push origin IMR-forked   # NOT main, NOT HEAD
```

- Use conventional commits: `feat:`, `fix:`, `refactor:`, `style:`, `chore:`, `docs:`
- Never run `git push origin main` or `git push --force`
- After every session push, confirm with `git log --oneline -3`

---

## 3. Project Structure

```
D:\IMR-Forked\
├── backend/
│   ├── app/
│   │   ├── api/routers/recommend.py    ← Main recommendation endpoint
│   │   ├── core/
│   │   │   ├── mood_cache_service.py   ← MoodCacheService (cache logic + locks)
│   │   │   ├── mood_tmdb_mapping.py    ← MOOD → TMDB query config (edit to tune moods)
│   │   │   ├── tmdb_service.py         ← HTTP calls to TMDB, image base URL cache
│   │   │   ├── llm_service.py          ← Gemini mood inference
│   │   │   ├── fusion.py               ← Score blending
│   │   │   ├── ranking.py              ← Final ranking
│   │   │   ├── filters.py              ← Content filters
│   │   │   └── config.py               ← Settings (reads .env)
│   │   ├── db/
│   │   │   ├── models.py               ← SQLAlchemy models incl. MoodMovieCache
│   │   │   ├── session.py              ← DB engine + SessionLocal
│   │   │   └── seed_data.py            ← Initial catalog seed
│   │   ├── schemas/
│   │   │   ├── recommendation.py       ← Response schema (tmdb_id, tmdb_url optional)
│   │   │   └── mood.py
│   │   ├── poster_cache/
│   │   │   └── tmdb_config.json        ← Disk-cached TMDB image base URL
│   │   └── main.py                     ← FastAPI app + lifespan (creates tables)
│   ├── tests/
│   │   ├── test_api.py
│   │   ├── test_filters.py
│   │   └── test_ranking.py
│   ├── .venv/                          ← Python virtualenv
│   ├── moodreel.db                     ← SQLite database
│   ├── requirements.txt
│   └── pytest.ini
├── frontend/
│   ├── src/
│   │   ├── App.tsx                     ← Root component, mood → recommend flow
│   │   ├── components/
│   │   │   ├── mood/                   ← Mood input UI
│   │   │   ├── results/MovieCard.tsx   ← Poster + title, links to TMDB
│   │   │   ├── filters/                ← Filter controls
│   │   │   └── safety/                 ← Safety check UI
│   │   ├── services/api.ts             ← getRecommendations(), moodName param
│   │   └── types.ts                    ← MovieRecommendation type
│   ├── package.json
│   └── vite.config.ts
├── package.json                        ← Root; has `concurrently` for `npm run dev`
├── start_app.bat                       ← Windows launch script
└── .agents/skills/imr-project/SKILL.md ← THIS FILE
```

---

## 4. Dev Commands

### Start Everything (Recommended)
```powershell
cd D:\IMR-Forked
npm install          # only needed once or after package.json changes
npm run dev          # starts backend (port 8000) + frontend (port 5173) concurrently
```

### Backend Only
```powershell
cd D:\IMR-Forked\backend
.\.venv\Scripts\uvicorn app.main:app --reload --port 8000
```

### Frontend Only
```powershell
cd D:\IMR-Forked
npm --prefix frontend run dev
```

### URLs when running
| Service | URL |
|---|---|
| Frontend | http://localhost:5173 |
| Backend API | http://127.0.0.1:8000 |
| API Docs (Swagger) | http://127.0.0.1:8000/docs |
| Health check | http://127.0.0.1:8000/health |

---

## 5. Testing & Verification

> [!IMPORTANT]
> Run BOTH of these after every backend change, and the build check after every frontend change. Never push with failing tests.

```powershell
# Backend tests (must be 17/17 passing)
.\backend\.venv\Scripts\pytest backend\tests -v

# Frontend TypeScript build (must be 0 errors)
npm --prefix frontend run build

# Quick API smoke test
Invoke-WebRequest -Uri "http://127.0.0.1:8000/health" -Method Get | Select-Object -ExpandProperty Content
```

---

## 6. Architecture: Mood Cache System

The core performance architecture — understand this before changing recommendation flow.

```
User Request (mood)
       │
       ▼
MoodCacheService.get_recommendations()
       │
       ├─ [CACHE HIT] → SQLite query → return instantly (0 TMDB calls, ~11ms)
       │
       └─ [CACHE MISS]
              │
              ├─ Acquire per-mood threading.Lock (prevents duplicate fetches)
              │
              ├─ TMDB /discover/movie (2 pages = ~40 movies)
              │   └─ Timeout: 6s, Max retries: 2
              │
              ├─ Store in `mood_movie_cache` table (expires in 7 days)
              │
              └─ Release lock → return results (~2.8s first time)
```

### Key Files for Cache

| File | Purpose |
|---|---|
| `backend/app/core/mood_tmdb_mapping.py` | **Edit this to tune moods** — genre IDs, sort order, filters per mood |
| `backend/app/core/mood_cache_service.py` | Cache read/write logic + concurrency locks |
| `backend/app/db/models.py` | `MoodMovieCache` SQLAlchemy model |
| `backend/app/poster_cache/tmdb_config.json` | Disk-persisted TMDB image base URL |

### Cache Expiry & Refresh
- Default TTL: **7 days** (set in `mood_tmdb_mapping.py::DEFAULT_CACHE_EXPIRY_DAYS`)
- Manual refresh endpoint: `POST /api/v1/recommendations/refresh-mood/{mood_key}`
- Mood mapping inspector: `GET /api/v1/recommendations/mood-mapping`

### Movie Data Stored (ONLY these fields)
```python
tmdb_id, title, poster_path, backdrop_path, release_year
```
**No** synopsis, cast, rating, trailers, reviews, or credits are stored.

---

## 7. TMDB Integration Rules

> [!WARNING]
> TMDB genre IDs use `|` (pipe) for OR, `,` (comma) for AND.
> Comma-AND is very restrictive and often returns 0 results. Always use pipe-OR.

```python
# CORRECT — OR logic (broader results)
"with_genres": "10749|18"   # Romance OR Drama

# WRONG — AND logic (too restrictive, often 0 results)
"with_genres": "10749,18"   # Romance AND Drama (must have both)
```

### TMDB Genre ID Reference
```
Action: 28     | Adventure: 12  | Animation: 16  | Comedy: 35
Crime: 80      | Documentary: 99| Drama: 18      | Family: 10751
Fantasy: 14    | History: 36    | Horror: 27     | Music: 10402
Mystery: 9648  | Romance: 10749 | Sci-Fi: 878    | Thriller: 53
War: 10752     | Western: 37
```

### TMDB Image URLs
- Base URL is fetched from TMDB `/configuration` endpoint and cached to disk at `backend/app/poster_cache/tmdb_config.json`
- **Never hardcode** `https://image.tmdb.org/t/p/` — always use `tmdb_service.get_image_base_url()`
- Size used: `w500` for posters

### TMDB Attribution (Legal Requirement)
The frontend footer must always show:
1. The official TMDB logo (`https://www.themoviedb.org/assets/2/v4/logos/v2/blue_short-8e7b30f73a4020692ccca9c88bafe5dcb6f8a62a4c6bc55cd9ba82bb2cd95f6c.svg`)
2. This exact text: *"This product uses the TMDB API but is not endorsed or certified by TMDB."*
3. TMDB logo must be visually less prominent than MoodReel branding.

---

## 8. Movie Card Behavior

Each `MovieCard` shows **only**:
- Poster image (lazy-loaded, `loading="lazy"`)
- Movie title

Each card is an `<a>` tag linking to:
```
https://www.themoviedb.org/movie/{tmdb_id}
```
with `target="_blank" rel="noopener noreferrer"`.

**No rating, synopsis, cast, or other detail is shown in the app.**

---

## 9. Schema Constraints

`MovieRecommendation` in `frontend/src/types.ts` — fields marked `?` are optional:
```typescript
interface MovieRecommendation {
  id: number;
  title: string;
  tmdb_id?: number;
  tmdb_url?: string;
  poster_url?: string;
  mood_compatibility?: number;   // Optional — not present for TMDB-cached results
  safety_check?: object;         // Optional
}
```

> [!NOTE]
> `WhyThisModal` references `mood_compatibility` which may be undefined for TMDB-cached
> recommendations. If the modal crashes, guard with optional chaining (`?.`) or conditionally
> hide it for cache-sourced movies.

---

## 10. Known Issues & Historical Fixes

| Issue | Fix Applied |
|---|---|
| `sqlite3.OperationalError: no such column: titles.origin` | Stale `moodreel.db`. Fix: delete both `moodreel.db` files, restart backend to recreate tables |
| `'concurrently' is not recognized` | Run `npm install` at repo root to install `concurrently` dev dependency |
| TMDB discover returning 0 results for a mood | Comma-AND genre filter too restrictive → switch to pipe-OR in `mood_tmdb_mapping.py` |
| `vote_average_gte` blocking all results | Remove `vote_average_gte` from that mood's config in `mood_tmdb_mapping.py` |
| `curl` output JSON parse failure | `rsplit("\n", 1)` separates body from status code appended by `\n%{http_code}` format |
| `mood_input_json is an invalid keyword argument for EventLog` | Column is `mood_input` (not `mood_input_json`) in the EventLog SQLAlchemy model |

### Reset the Database (if schema mismatch)
```powershell
Remove-Item "D:\IMR-Forked\backend\moodreel.db" -ErrorAction SilentlyContinue
Remove-Item "D:\IMR-Forked\moodreel.db" -ErrorAction SilentlyContinue
# Restart backend — tables recreated automatically via Base.metadata.create_all()
```

---

## 11. Environment Variables

```
# backend/.env  (never commit this file)
TMDB_API_KEY=...
GEMINI_API_KEY=...
DATABASE_URL=sqlite:///./moodreel.db
```

The `backend/app/core/config.py` reads these via Pydantic `BaseSettings`.

---

## 12. Performance Benchmarks (Reference)

| Scenario | Response Time | TMDB Calls |
|---|---|---|
| First request (uncached mood) | ~2,800 ms | 2 (`/discover/movie` × 2 pages + `/configuration`) |
| Second request (cached mood) | ~11 ms | **0** |
| Concurrency test (2 simultaneous uncached) | ~2,800 ms | **1** (lock prevents duplicate) |

---

## 13. What NOT to Do

- ❌ Do NOT call TMDB `/movie/{id}`, `/credits`, `/videos`, `/reviews`, or `/images` per movie
- ❌ Do NOT run `enrich_movie()` in the request path (it was the original 13s bottleneck)
- ❌ Do NOT hardcode TMDB image base URLs
- ❌ Do NOT push to `main` branch
- ❌ Do NOT change unrelated features when fixing a bug
- ❌ Do NOT skip pytest before pushing
- ❌ Do NOT use comma-AND for TMDB `with_genres` (use `|` pipe-OR)
