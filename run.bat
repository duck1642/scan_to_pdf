@echo off
start "" cmd /k "cd /d %~dp0backend && venv\Scripts\python app.py"
start "" cmd /k "cd /d %~dp0frontend && npm run dev"

:: Wait 2 seconds for Vite to initialize, then automatically open the UI in your default browser
timeout /t 2 >nul
start http://localhost:5173
