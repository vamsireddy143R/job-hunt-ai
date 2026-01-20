@echo off
echo ==========================================
echo      JOBHUNT AI - ONE CLICK SETUP
echo ==========================================

REM Detect Python Command
where py >nul 2>nul
if %errorlevel% equ 0 (
    set PYTHON_CMD=py
) else (
    set PYTHON_CMD=python
)
echo Using Python command: %PYTHON_CMD%

echo [1/4] Installing Backend Dependencies...
cd server
%PYTHON_CMD% -m pip install -r requirements.txt
cd ..

echo [2/4] Installing Frontend Dependencies...
cd client
call npm install
call npm install -D tailwindcss postcss autoprefixer
call npm install lucide-react framer-motion axios
cd ..

echo [3/4] Starting Backend Server...
start "JobHunt API" cmd /k "cd server && %PYTHON_CMD% -m uvicorn main:app --reload --port 8000"

echo [4/4] Starting Frontend Client...
start "JobHunt UI" cmd /k "cd client && npm run dev"

echo ==========================================
echo      APP IS RUNNING!
echo      Frontend: http://localhost:5173
echo      Backend: http://localhost:8000
echo ==========================================
pause
