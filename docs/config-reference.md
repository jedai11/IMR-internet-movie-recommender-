# IMR (Internet Movie Recommender) Configuration Reference

All settings are configured via `backend/app/core/config.py` and overrideable via environment variables (`.env`).

| Variable | Default | Purpose & Rationale |
|---|---|---|
| `PROJECT_NAME` | `"IMR API"` | Application identifier in OpenAPI and logs |
| `DATABASE_URL` | `"sqlite:///./imr.db"` | SQLite database connection for zero-dependency local runs |
| `GEMINI_API_KEY` | `None` | Optional Google Gemini API key for external LLM inference |
| `OPENAI_API_KEY` | `None` | Optional OpenAI key |
| `LLM_PROVIDER` | `"auto"` | Selection between `'auto'`, `'gemini'`, `'openai'`, or `'heuristic'` |
| `COLD_START_THRESHOLD` | `3` | Number of feedback ratings before shifting weights to established profile |
| `COLD_START_W_MOOD` | `0.90` | Mood weight for new/cold-start users |
| `COLD_START_W_TASTE` | `0.10` | Taste weight for new/cold-start users |
| `ESTABLISHED_W_MOOD` | `0.70` | Mood weight for users with $\ge 4$ ratings |
| `ESTABLISHED_W_TASTE` | `0.30` | Taste weight for users with $\ge 4$ ratings |
| `SHIFT_STEP_FACTOR` | `0.55` | Trajectory step $\lambda \in [0.4, 0.7]$ to regulate mood toward calm equilibrium |
| `DISTRESS_KEYWORDS` | `[...]` | High-priority crisis keywords checked by early safeguard |

