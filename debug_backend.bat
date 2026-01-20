@echo off
echo ==========================================
echo      JOBHUNT AI - BACKEND DEBUGGER
echo ==========================================

REM Detect Python
where py >nul 2>nul
if %errorlevel% equ 0 (
    set PYTHON_CMD=py
) else (
    set PYTHON_CMD=python
)

echo [1/3] Using Python: %PYTHON_CMD%

echo [2/3] Installing Dependencies (Force Upgrade)...
cd server
%PYTHON_CMD% -m pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install dependencies!
    pause
    exit /b
)

echo [3/3] Starting Server manually...
%PYTHON_CMD% -m uvicorn main:app --reload --port 8000

pause
