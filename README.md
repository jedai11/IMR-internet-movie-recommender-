# IMR (Internet Movie Recommender) / MoodReel

> **Affective Psychology • Deterministic Grounded Catalog • Designed with Privacy & Transparency in Mind**

**IMR (Internet Movie Recommender)**, powered by the **MoodReel** engine, maps human emotional states into formal psychological affect space (**Russell’s Circumplex Model of Affect: Valence $\times$ Arousal**) and deterministically matches them against catalog titles with zero hallucinated movies.

---

## Key System Features

- **Russell's Circumplex Affect Space:** Continuous 2D affective canvas ($v \in [-1.0, 1.0]$ for Valence, $a \in [-1.0, 1.0]$ for Arousal) paired with 8 instant emotion presets (*Joyful, Peaceful, Melancholic, Anxious, Energized, Exhausted, Angry, Hopeful*).
- **Grounded Catalog & Zero Hallucination:** Movies, genres, runtimes, trigger warnings, and streaming availability are strictly queried from verified database tables. The LLM never invents titles or computes scores.
- **Dual Strategy Modes:**
  - **Catharsis:** Validates and mirrors your current state ("Meet me where I am").
  - **Shift:** Calculates an emotional regulation trajectory vector to gently guide state toward warmth and equilibrium ("Gently lift or soothe me").
- **Strict UNKNOWN-Metadata Defense:** When trigger exclusions are selected, any title with verified warnings *or unverified status (`UNKNOWN`)* is strictly dropped rather than assumed safe.
- **Early Distress Safeguard & International Crisis Helplines:** High-priority crisis detection scans user free-text. If acute distress or self-harm ideation is detected, recommendation logic is immediately bypassed to surface supportive, confidential crisis resources:
  - **United States & Canada:** Call or text **988** ([988 Lifeline](https://988lifeline.org))
  - **Crisis Text Line:** Text **HOME to 741741** (US & Canada) or **85258** (UK)
  - **United Kingdom & Ireland:** Call **116 123** ([Samaritans](https://www.samaritans.org)) or **111** (NHS)
  - **India:** Call **14416** ([Tele-MANAS](https://telemanas.mohfw.gov.in)) or **1800-599-0019** (KIRAN)
  - **Worldwide:** Free confidential support in 130+ countries via [Find A Helpline](https://findahelpline.com) & [Befrienders Worldwide](https://www.befrienders.org)
- **"Why this?" Transparency Inspector:** Provides full mathematical visibility into Euclidean distances, fit scores, and safety filter audits.
- **Privacy-by-Design & Data Minimization:** Sensor-free manual input baseline with zero biometric tracking or webcams. Sessions are pseudonymous with a 1-click full session wipe.

---

## Quickstart Guide

### Prerequisites
- Python 3.10+
- Node.js 18+ & npm

### One-Click Launch (Windows)
Run the included launcher script:
```bat
start_app.bat
```
This safely starts the backend locally on `http://127.0.0.1:8000` and the frontend on `http://localhost:5173`.

### Manual Launch

#### 1. Start the Backend API (FastAPI)

```bash
cd backend

# On Windows (PowerShell):
.\.venv\Scripts\Activate.ps1
python run_backend.py

# Or without activating:
.\.venv\Scripts\python.exe run_backend.py
```
Backend will start on: **http://127.0.0.1:8000**  
Interactive Swagger docs: **http://127.0.0.1:8000/docs**

#### 2. Start the Frontend UI (React + Vite + Tailwind)

```bash
cd frontend
npm run dev
```
Frontend will start on: **http://localhost:5173**

---

## Running Automated Tests

Run the complete backend test suite (unit tests, property tests, safety tests, and end-to-end API integration):

```bash
cd backend
.\.venv\Scripts\pytest -v
```

All 15 tests verify:
- Crisis phrases trigger distress response with 24/7 helplines
- Benign phrases pass cleanly
- Hard filters enforce max runtime and genre exclusion
- `UNKNOWN`-metadata defense drops unverified trigger titles
- Affective distance calculation and cold-start weighting behavior
- Full end-to-end API requests

---

## Project Structure

```
IMR-internet-movie-recommender-/
├── backend/
│   ├── app/
│   │   ├── api/routers/        # mood, recommend, feedback, catalog
│   │   ├── core/               # distress safeguard, fusion, shift, filters, ranking, llm
│   │   ├── db/                 # models, session, seed catalog
│   │   ├── schemas/            # Pydantic v2 validation contracts
│   │   └── main.py             # FastAPI entrypoint + CORS + Lifespan
│   ├── tests/                  # Pytest test suite
│   ├── requirements.txt
│   └── run_backend.py
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── mood/           # MoodCanvas, EmotionPresets, StrategySelector
│   │   │   ├── filters/        # FilterDrawer with UNKNOWN-defense toggle
│   │   │   ├── results/        # MovieCard, WhyThisModal
│   │   │   └── safety/         # ConsentNotice, DistressBanner, PrivacyCenterModal
│   │   ├── services/api.ts     # Typed API client
│   │   ├── types.ts            # TypeScript contracts
│   │   └── App.tsx             # Application shell
│   ├── package.json
│   └── vite.config.ts
│
├── docs/                       # Architecture, config reference, privacy principles
├── LICENSE                     # MIT Open Source License
└── start_app.bat               # Safe local launcher (127.0.0.1)
```

---

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
