#!/bin/bash

echo "Starting Tamil-English Translator..."
echo ""

SCRIPT_DIR="$(dirname "$0")"

# Start Flask backend in background
"$SCRIPT_DIR/start-backend.sh" &
BACKEND_PID=$!

# Wait for backend to start
sleep 3

# Start React frontend
"$SCRIPT_DIR/start-frontend.sh" &
FRONTEND_PID=$!

echo ""
echo "Both servers are starting..."
echo "Flask Backend: http://localhost:5000"
echo "React App: http://localhost:3001"
echo ""
echo "Press Ctrl+C to stop all servers"

# Wait for both processes
wait
