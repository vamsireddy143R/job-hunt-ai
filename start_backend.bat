@echo off
echo ==========================================
echo      JOBHUNT AI - BACKEND
echo ==========================================

REM Detect Python
where py >nul 2>nul
if %errorlevel% equ 0 (
    set PYTHON_CMD=py
) else (
    set PYTHON_CMD=python
)

echo [1/2] Checking Dependencies...
cd server
%PYTHON_CMD% -m pip install -r requirements.txt
echo.

echo [2/2] Starting Brain...
echo.
echo    WAIT for: "Uvicorn running on http://0.0.0.0:8000"
echo.
%PYTHON_CMD% -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload

echo.
echo [SERVER CRASHED] - Copy the error above if it happens.
pause
