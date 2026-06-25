@echo off
start "" cmd /k "cd /d %~dp0backend && venv\Scripts\python app.py"
start "" cmd /k "cd /d %~dp0frontend && npm run dev"
