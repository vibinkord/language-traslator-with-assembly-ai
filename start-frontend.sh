#!/bin/bash

echo "Starting React Frontend..."
echo ""

cd "$(dirname "$0")/react-translator"

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "Installing dependencies..."
    npm install
    echo ""
fi

# Start the development server
echo "Starting React Dev Server on http://localhost:3001"
echo ""
npm run dev
