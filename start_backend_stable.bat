@echo off
echo ==========================================
echo      JOBHUNT AI - STABLE SERVER
echo ==========================================

REM Detect Python
where py >nul 2>nul
if %errorlevel% equ 0 (
    set PYTHON_CMD=py
) else (
    set PYTHON_CMD=python
)

echo [1/2] Installing Dependencies...
cd server
%PYTHON_CMD% -m pip install -r requirements.txt >nul 2>nul

echo [2/2] Starting Server (Production Mode)...
echo.
echo    If successful, you will see: "Uvicorn running on http://0.0.0.0:8000"
echo.
%PYTHON_CMD% -m uvicorn main:app --host 0.0.0.0 --port 8000

pause
