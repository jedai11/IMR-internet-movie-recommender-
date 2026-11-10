@echo off
title IMR (Internet Movie Recommender) Launcher
echo ===================================================
echo   Starting IMR (Internet Movie Recommender)
echo ===================================================
echo.

echo [1/2] Launching Backend on http://localhost:8000 ...
start "IMR Backend (Port 8000)" cmd /k "cd /d %~dp0backend && .venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000"

echo [2/2] Launching Frontend on http://localhost:5173 ...
start "IMR Frontend (Port 5173)" cmd /k "cd /d %~dp0frontend && npm run dev"

echo.
echo ===================================================
echo Both services are now running!
echo Frontend: http://localhost:5173
echo Backend:  http://localhost:8000
echo ===================================================

