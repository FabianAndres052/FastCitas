@echo off
echo Iniciando FastCitas...
start cmd /k "cd /d %~dp0backend && python -m uvicorn main:app --reload"
timeout /t 3 /nobreak >nul
start cmd /k "cd /d %~dp0frontend && npm run dev"
timeout /t 4 /nobreak >nul
start http://localhost:5173