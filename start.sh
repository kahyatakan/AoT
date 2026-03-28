#!/bin/bash
# start.sh — Anvil of Taylor'ı tek komutla başlat
# Kullanım: ./start.sh
# Durdurmak için: Ctrl+C

echo "Anvil of Taylor baslatiliyor..."

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"

# Backend (arka planda)
python -m uvicorn server.main:app --reload --port 8000 &
BACKEND_PID=$!

# Frontend (arka planda)
cd "$ROOT_DIR/web" && npm run dev &
FRONTEND_PID=$!

echo "   Backend  -> http://localhost:8000"
echo "   Frontend -> http://localhost:5173"
echo "   Durdurmak icin Ctrl+C"

# Tarayıcıyı aç
sleep 2.5
python -c "import webbrowser; webbrowser.open('http://localhost:5173')"

# Ctrl+C ile ikisini de kapat
trap "echo ''; echo 'Kapatiliyor...'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit 0" INT TERM

wait
