@echo off
start "" cmd /c "cd /d %~dp0backend && venv\Scripts\activate && python app.py"
start "" cmd /c "cd /d %~dp0frontend && npm run dev"
