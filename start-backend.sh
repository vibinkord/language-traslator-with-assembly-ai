#!/bin/bash

echo "Starting Flask Backend..."
echo ""

cd "$(dirname "$0")/Vibin_Translator_1/Code"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
source venv/bin/activate 2>/dev/null || . venv/Scripts/activate

# Install/update requirements
echo "Installing dependencies..."
pip install -q -r requirements.txt

# Start Flask server
echo ""
echo "Starting Flask Server on http://localhost:5000"
echo ""
python main.py
