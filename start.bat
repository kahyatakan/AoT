@echo off
echo Anvil of Taylor baslatiliyor...
echo    Backend  -^> http://localhost:8000
echo    Frontend -^> http://localhost:5173
echo    Durdurmak icin bu pencereyi kapatin.
echo.

cd /d "%~dp0"

start "AOT Backend" /B python -m uvicorn server.main:app --reload --port 8000

cd web
start "AOT Frontend" /B npm run dev

timeout /t 3 >nul
start http://localhost:5173

echo Sunucular calisiyor. Durdurmak icin bu pencereyi kapatin.
pause
