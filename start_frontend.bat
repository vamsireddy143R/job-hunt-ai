@echo off
echo ==========================================
echo      JOBHUNT AI - FRONTEND
echo ==========================================

cd client

echo [1/2] Checking Node Modules...
call npm install
echo.

echo [2/2] Starting Website...
echo.
call npm run dev

pause
