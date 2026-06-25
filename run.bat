@echo off
title scan_to_pdf Launcher
echo =========================================
echo       Starting scan_to_pdf Application
echo =========================================
echo.

:: 1. Start the Flask Backend
echo [1/2] Launching Flask Backend...
start "scan_to_pdf - Flask Backend" cmd /k "cd /d %~dp0backend && venv\Scripts\activate && python app.py"

:: 2. Start the Svelte Frontend
echo [2/2] Launching Svelte Frontend...
start "scan_to_pdf - Svelte Frontend" cmd /k "cd /d %~dp0frontend && npm run dev"

echo.
echo -----------------------------------------
echo Backend:  http://127.0.0.1:5000
echo Frontend: http://localhost:5173
echo -----------------------------------------
echo.
echo Both servers have been launched in separate windows.
echo You can close this window now.
echo.
pause
