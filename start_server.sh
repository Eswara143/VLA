#!/usr/bin/env bash
# Unitree G1 Datasets Hub Launcher

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PORT=8085

echo "=================================================="
echo " Starting Unitree G1 Datasets Web Hub on port $PORT"
echo " Directory: $DIR"
echo " URL: http://localhost:$PORT"
echo "=================================================="

# Check if port is already in use
if lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo "Server is already running on port $PORT."
else
    # Start python http server in background
    nohup python3 -m http.server $PORT --directory "$DIR" > /dev/null 2>&1 &
    sleep 1
    echo "Server started successfully!"
fi

# Try to open in default browser if xdg-open exists
if command -v xdg-open >/dev/null 2>&1; then
    xdg-open "http://localhost:$PORT" >/dev/null 2>&1 &
fi

echo "Open in your browser: http://localhost:$PORT"
