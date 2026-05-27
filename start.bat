@echo off
echo Starting backend...
start "Backend" cmd /k "cd /d %~dp0python\backend && py -m uvicorn main:app --reload --port 8000"

timeout /t 2 /nobreak > nul

echo Starting frontend...
start "Frontend" cmd /k "cd /d %~dp0python\frontend && npm run dev"

echo.
echo Backend: http://127.0.0.1:8000
echo Frontend: http://localhost:5173
echo.