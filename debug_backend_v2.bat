@echo off
echo ==========================================
echo      JOBHUNT AI - BACKEND DEBUGGER V2
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
%PYTHON_CMD% -m pip install -r requirements.txt
echo.

echo [2/2] Starting Server...
echo.
%PYTHON_CMD% -m uvicorn main:app --host 0.0.0.0 --port 8000
echo.
echo [SERVER STOPPED]
echo If you see an error above, please copy it.
pause
